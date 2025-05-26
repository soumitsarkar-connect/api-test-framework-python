import os
import subprocess
import sys
import emoji


def print_with_emoji(emoji_name, message):
    """Prints message with emoji."""
    print(emoji.emojize(f":{emoji_name}:\u00A0 {message}", language="alias"))


def run_command(command, shell=False):
    """Runs a shell command and checks for errors."""
    try:
        subprocess.run(command, shell=shell, check=True)
        print_with_emoji("check_mark_button", "Success!\n")

    except subprocess.CalledProcessError as e:
        print_with_emoji("cross_mark", "Failure!\n")

    except KeyboardInterrupt:
        print("")


# Print setup header
print("")
print("=" * 40)
print_with_emoji("hammer_and_wrench", "Setting up RealTime API Test Automation Project")
print("=" * 40)

# Create virtual environment
print_with_emoji("gear", "Creating virtual environment...")
run_command("invoke create-venv", shell=True)

# Install dependencies
print_with_emoji("package", "Installing dependencies...")
run_command("invoke install-dependencies", shell=True)

# Print test execution header
print("")
print("=" * 20)
print_with_emoji("test_tube", "Running Tests")
print("=" * 20)

# Run tests and generate Allure report
print_with_emoji(
    "magnifying_glass_tilted_left", "Running tests and generating Allure test report..."
)
run_command("invoke run-tests", shell=True)
