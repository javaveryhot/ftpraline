import os, sys, time, logging, json, shutil
from flask import Flask, request
from multiprocessing import Process

inittime = None

os.system("clear")

app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)
os.environ["WERKZEUG_RUN_MAIN"] = "true"


FTPPrefix = "/ftp"


@app.route("/__ftpraline")
def showlist():
    return "This server is running FTPraline."

@app.route("/__ftpraline/<reqname>", methods=["POST"])
def ftprequest(reqname):
    password = request.form.get("password")
    if password != os.getenv("ftpraline_password"):
      return "3"

    if reqname == "auth":
      return "2"
    elif reqname == "read":
      rpath = request.form.get("path") or ""
      if os.path.isfile(rpath):
        f = open(rpath, "r")
        try:
          fcontent = f.read()
        except:
          return "9"
        f.close()
        fstat = os.stat(rpath)
        robj = {
          "type": 1,
          "content": fcontent,
          "mdate": fstat.st_mtime,
          "size": fstat.st_size,
          "path": os.path.realpath(rpath),
          "parentpath": os.path.abspath(os.path.join(rpath, os.pardir))
        }
        return json.dumps(robj)
      elif os.path.isdir(rpath) or rpath == "":
        if rpath == "":
          rpath = os.getcwd()
        diritems = []
        try:
          items = os.listdir(rpath)
        except:
          return "8"
        for i in items:
          stat = os.stat(os.path.join(rpath, i))
          diritems.append({
            "name": i,
            "type": 0 if os.path.isdir(os.path.join(rpath, i)) else 1,
            "path": os.path.realpath(os.path.join(rpath, i)),
            "mdate": stat.st_mtime,
            "size": stat.st_size
          })
        return json.dumps({"type": 0, "path": os.path.realpath(rpath), "parentpath": os.path.abspath(os.path.join(rpath, os.pardir)), "children": diritems})
      else:
        return "5"
    elif reqname == "put":
      rlist = json.loads(request.form.get("list"))
      for req in rlist:
        rtype = req.get("type")
        ppath = req.get("path")
        if os.path.exists(ppath) or ppath == "":
          if rtype == "delete":
            if os.path.isfile(ppath):
              os.remove(ppath)
            else:
              shutil.rmtree(ppath)
          elif rtype == "make_f":
            name = req.get("name")
            path = os.path.join(ppath, name)
            if os.path.exists(path):
              continue
            f = open(path, "w")
            if req.get("content") is not None:
              f.write(req.get("content"))
            f.close()
          elif rtype == "make_d":
            name = req.get("name")
            makepath = os.path.join(ppath, name)
            if os.path.exists(makepath):
              continue
            os.mkdir(makepath)
          elif rtype == "change_f":
            if req.get("content") is not None:
              f = open(ppath, "w")
              f.write(req.get("content"))
              f.close()
            if req.get("new_name") is not None:
              os.rename(ppath, os.path.join(os.path.abspath(os.path.join(ppath, os.pardir)), req.get("new_name")))
          elif rtype == "change_d":
            if req.get("new_name") is not None:
              os.rename(ppath, os.path.join(os.path.abspath(os.path.join(ppath, os.pardir)), req.get("new_name")))
        else:
          return "5"
      return "2"
    else:
      return "4"





@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response


def run():
    app.run(host="0.0.0.0", port=5000)

def server():
    global FTPPrefix
    server = Process(target=run)
    server.start()
    os.system("clear")
    print(f"\033[33mUsing FTPraline, took {round(time.time() - inittime, 2)}s.\nType \"" + FTPPrefix + "help\" for help.\033[0m")
    main = Process(target=ExeMain)
    main.start()
    while True:
      ftprcommand = input()
      if ftprcommand.startswith(FTPPrefix):
        ftprcommand = ftprcommand[len(FTPPrefix):]
      else:
        continue
      if ftprcommand == "help":
        print("\033[33mHELP\033[0m")
      elif ftprcommand == "stop":
        server.terminate()
        print("\033[31mStopped FTPraline server.\033[0m")
        break
      elif ftprcommand == "restart":
        print("\033[33mRestarting FTPraline server...\033[0m")
        server.terminate()
        init()
      elif ftprcommand == "github":
        print("https://github.com/javaveryhot/ftpraline")
      else:
        print("\033[31mUnknown FTPraline console command.\033[0m")


def ExeMain():
    if os.getenv("ftpraline_execute_main") != "no":
      os.system("python3 main.py")


def init():
  if os.getenv("ftpraline_prefix_override"):
    global FTPPrefix
    FTPPrefix = os.getenv("ftpraline_prefix_override")
  global inittime
  inittime = time.time()
  if os.getenv("ftpraline_password") is not None:
    server()
  else:
    print("\033[31mYou have not set an FTPraline password. Put it in a \".env\" file as \"ftpraline_password=mypasswordhere\".\033[0m")

if __name__ == "__main__":
  init()
