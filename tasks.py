from invoke import task
import os
import signal
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)

# Command to Activate virtual environment (Windows/Unix/Mac)
activate_cmd = (
    "venv\\Scripts\\activate" if os.name == "nt" else "source venv/bin/activate"
)


def run_command(command):
    """Run command"""
    print(Style.BRIGHT + Fore.YELLOW + command)

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=None,
            stderr=None,
        )

        # Wait for the process to finish (blocks execution)
        process.wait()

    except KeyboardInterrupt:
        print("")
        process.send_signal(signal.SIGTERM)  # Terminate process safely
    except Exception as e:
        print(f"Unexpected error: {e}")


@task
def create_venv(c):
    """Create a virtual environment."""
    run_command("python -m venv venv")


@task
def install_dependencies(c):
    """Activate virtual environment and install dependencies."""
    run_command(f"{activate_cmd} && pip install -r requirements.txt")


@task
def run_tests(c):
    """Run Behave tests and generate an Allure report."""
    run_command(f"{activate_cmd} && behave -f allure -o reports/allure-report")


@task
def view_report(c):
    """View Allure report."""
    run_command(f"{activate_cmd} && allure serve reports/allure-report")


@task
def setup_and_run(c):
    """Run all steps in sequence."""
    create_venv(c)
    install_dependencies(c)
    run_tests(c)
    view_report(c)
