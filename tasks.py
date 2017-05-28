from invoke import task

base_dir = "feb_test"

local_env_settings = {
    "server_name": "ubuntu",
    "host": "52.79.170.101",
    "pem_file_path": "Downloads/3g_admin_panel.pem"
}


server_login_string = "ssh -i {pem_file_path} {server_name}:{host}"
server_dump_string = "TODO"


@task
def connect_to_server(ctx):
    print("Start requirement install")
    print(server_login_string.format(**local_env_settings))
    ctx.run("sudo ssh -i ~/Downloads/3g_admin_panel.pem ubuntu@52.79.170.101")
    print("::::::: Requirement installation is Done :::::::")


@task(connect_to_server)
def create_virtual_env(ctx, activate=True):
    print("Under create virtual env ...")
    ctx.run("sudo apt-get install virtualenv")
    ctx.run("virtualenv -p python3 "+base_dir+"/env")
    ctx.run("source "+base_dir+"/env/bin/activate")
    print("::::::: Virtual env is Activated :::::::")


@task(create_virtual_env, help={"op": "set operation name for git", "branch": "provide branch name"})
def get_from_git(ctx, op=None):
    print("Clone repo from git")
    # ctx.run("cd ppppp")
    if not op:
        ctx.run("git clone https://github.com/grv07/3g-dashboard "+base_dir+"/3g-dashboard")
    print("::::::: Git clone is Done :::::::")


@task(get_from_git)
def download_req_s(ctx):
    print("Start requirement install")
    ctx.run("pip install -r requirement.txt")
    print("::::::: Requirement installation is Done :::::::")


@task(download_req_s, help={"new": "if try to build a new project"})
def build(ctx, new=False):
    """
    Build a sphinx docs on docs folder
    :param ctx:
    :param new: if new setup default:False
    :return:
    """
    print("Start Build ...")

    # ctx.run("mkdir "+base_dir)
    ctx.run("cd " + base_dir)
    # ctx.run("touch "+base_dir+"/form_filter")
    # ctx.run(server_login_string.format(**local_env_settings))

    # the filename, or list of file-names, of optional private key(s)
    # to try for authentication

    if new:
        pass
    print("Congrats, Build complete! Have Fun :)")


@task(help={"clean": "Send true if you want to clean first"})
def build_docs(ctx, clean=False):
    """
    Build a sphinx docs on docs folder
    :param ctx:
    :param clean: By default False
    :return:
    """
    if clean:
        ctx.run("make clean")
    ctx.run("sphinx-build docs docs/_build")

