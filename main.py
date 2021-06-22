import subprocess
import sys


args = sys.argv
return_value = subprocess.run(["echo", "Hello World"])
print(return_value)
print(type(return_value))
print(repr(return_value))
print(args)

return_value = subprocess.run(["echo", f"cmd arguments are: {' '.join([arg for arg in args ])}"])
print(return_value.args)
print(return_value.returncode)
print(return_value.stdout)
print(return_value.stderr)
print(return_value.check_returncode())


return_value = subprocess.run(["mount"])

