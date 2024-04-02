from swift:5.10

from python:3.12-slim
run apt-get update -y && apt-get install -y git && pip install flit
add . /tmp/build/
run (cd /tmp/build; flit build)

from python:3.12-slim
copy --from=0 /usr/bin/swift-demangle /usr/local/bin/
copy --from=0 /usr/lib/swift/linux/libswiftCore.so /usr/local/lib/swift/linux/
copy --from=1 /tmp/build/dist/*.whl /tmp/dist/
run pip install /tmp/dist/*.whl
run mkdir /out
workdir /out
env in_container 1
cmd ["uvicorn", "demangle.apid:app", "--no-access-log", "--host", "0.0.0.0", "--port", "80"]
