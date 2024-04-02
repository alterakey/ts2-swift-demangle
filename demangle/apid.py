from __future__ import annotations
from typing import TYPE_CHECKING
from os import read, write, environ
from fastapi import FastAPI

if TYPE_CHECKING:
  from typing import Any, Mapping, Optional, Tuple

class Demangler:
  _f: Optional[Tuple[int, int]] = None

  def __init__(self, simplify: bool = False) -> None:
    from asyncio import Lock, Event, get_running_loop
    self._l = get_running_loop()
    self._w = Event()
    self._s = Lock()
    self._simp = simplify

  async def boot(self) -> None:
    def _do() -> None:
      from subprocess import Popen
      from os import openpty
      assert self._f is None
      i0, i1 = openpty()
      o0, o1 = openpty()
      with Popen(self._get_cmdline(), shell=True, bufsize=0, stdin=i1, stdout=o1) as _:
        self._f = (i0, o0)
        self._w.set()
      self._w.clear()
      self._f = None

    if not self._w.is_set():
      self._l.run_in_executor(None, _do)
      await self._w.wait()

  async def resolve(self, q: bytes) -> bytes:
    async with self._s:
      await self.boot()
      assert self._f
      write(self._f[0], q + b'\n')
      o = bytearray()
      while not o.endswith(b'\n'):
        o = o + read(self._f[1], 1024)
      return o.rstrip()

  def _get_cmdline(self) -> str:
    return '{}{}'.format(
      'swift-demangle' if environ.get('in_container') else 'swift demangle',
      ' -simplified' if self._simp else ''
    )


app = FastAPI()
dem0 = Demangler()
dem1 = Demangler(simplify=True)

@app.get("/{word}")
async def do(word: str) -> Mapping[str, Any]:
  return dict(to=await dem0.resolve(word.encode()))

@app.get("/s/{word}")
async def do_simpified(word: str) -> Mapping[str, Any]:
  return dict(to=await dem1.resolve(word.encode()))

def use_route_names_as_operation_ids(app: FastAPI) -> None:
  from fastapi.routing import APIRoute
  for route in app.routes:
    if isinstance(route, APIRoute):
      route.operation_id = route.name


use_route_names_as_operation_ids(app)
