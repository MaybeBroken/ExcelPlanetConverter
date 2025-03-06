import random
import subprocess
import os
from threading import Thread
import threading
from time import sleep
import atexit
import sys

if sys.platform == "win32":
    from tkinter import filedialog
elif sys.platform == "darwin":
    from PyQt5.QtWidgets import QFileDialog


# Make sure the script is running in its own directory
os.chdir(os.path.dirname(__file__))

DATALIST = []


# Register cleanup function to run on program exit
def cleanup(output_dir):
    if os.path.exists("convert.bat"):
        os.remove("convert.bat")
    try:
        for input_file, DATA in DATALIST:
            try:
                output_file = f"{output_dir}\\{input_file.removesuffix('.xlsx')}.csv"
                if os.path.exists(output_file):
                    os.remove(output_file)
            except Exception as e:
                print(f"Error deleting {output_file}: {e}")
    except Exception as e:
        print(f"Error deleting files: {e}")


# Sub-Program to convert the actual excel file to csv
batProgram = r"""
@echo off
echo Converting %1 to %2...
java -jar excelToCsv.jar --input %1 --sheet-name "System Builder" >> %2
echo Finished conversion, file saved to %2
"""


# Wrapper function to call the sub-program
def convert_excel_to_csv(input_file, output_file):
    """Takes an `input_file` and `output_file`,and converts the input file to a csvfile at the specified output path."""

    # Make sure the Converter is in the same directory as this script
    if not os.path.exists("excelToCsv.jar"):
        raise FileNotFoundError("The required excelToCsv.jar file is missing.")

    # Make sure the input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"The input file {input_file} does not exist.")

    # Ensure Java is on the system path
    try:
        if sys.platform == "win32":
            # run a dummy subprocess to check if Java is installed
            subprocess.run(
                ["java", "-version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        elif sys.platform == "darwin":
            # do the same on mac, but with the mac process manager
            os.spawnle(
                os.P_WAIT,
                "/usr/bin/java",
                "java",
                "-version",
                stdout=open(os.devnull, "w"),
                stderr=open(os.devnull, "w"),
            )
    # If Java is not installed, raise an error
    except Exception as e:
        raise EnvironmentError(
            "Java is not installed or not found in the system path: " + str(e)
        )
    converting = False
    # Run the program if the output file does not exist, otherwise read the file and return it
    if not os.path.exists(output_file):

        # Create the batch file
        with open("convert.bat", "w") as f:
            f.write(batProgram)

        def _thread():
            while converting:
                if os.path.exists(output_file):
                    # open the output file and print any added data
                    with open(output_file, "r") as f:
                        f.seek(0, os.SEEK_END)  # Move the cursor to the end of the file
                        while converting:
                            line = f.readline()  # Read the next line
                            if not line:
                                sleep(1)  # Wait for new entries
                                continue
                            else:
                                print(f"{line.strip()}")  # Print the added line
                                sleep(0.1)
                else:
                    sleep(1)

        converting = True
        Thread(target=_thread).start()
        # Run the batch file
        subprocess.run(["convert.bat", input_file, output_file])

    # Read the output file and return it
    with open(output_file, "r") as f:
        data = f.read()
    converting = False
    return data


# Convert letters to their corresponding index in the alphabet
def letter_to_int(scheme):
    scheme = scheme.upper()
    number = 0
    for i, char in enumerate(reversed(scheme)):
        number += (ord(char) - ord("A") + 1) * (26**i)
    return number


# Convert index in the alphabet to its corresponding letter
def int_to_letter(number):
    result = ""
    number -= 1
    while number >= 0:
        number, remainder = divmod(number, 26)
        result = chr(remainder + ord("A")) + result
        number -= 1
    return result


# Class to hold the definitions for the excel file, this knows where everything is
class Definitions:
    Star_Mass = "F:8"
    Surface_Temperature = "E:10"
    Luminosity = "E:11"
    Radius = "E:12"
    System_Age = "H:5"

    Suffix_Col = "K"
    Mass_Col = "L"
    Radius_Col = "P"
    Semimajor_Axis_Col = "T"
    Period_Days_Col = "U"
    Eccentricity_Col = "Z"
    Habitable_Zone_Col = "AJ"
    Tectonic_Habitability_Col = "AX"
    Rotation_Period_Col = "BC"

    Planet_Start_Row = 6
    Planet_End_Normal_Row = 30
    Planet_End_Max_Row = 101

    Base_XML_Start = """<resource fileversion="1">
	<maps>
		<map id="Milky Way D" name="Milky Way D" dimensions="800 10 240" systems="1"
            show-influence="false" seed="10101" autogenerate="false">
			<description />
			<pedia />
			<sector-mode>Alphanumeric</sector-mode>
			<sector-size>10 10</sector-size>
			<skybox source="base" />
			<background source="/images/nebula.png" style="Cover" scale="1" />
"""
    Base_XML_End = """
			<objects />
		</map>
	</maps>
</resource>"""


def run(InDir, OutDir):
    if not InDir or not OutDir:
        exit("No directories selected")

    # Initialize the data list
    DATALIST = []

    # Get a list of excel files in the input directory
    input_files = [f for f in os.listdir(InDir) if f.endswith(".xlsx")]

    # If there are no files, exit
    if not input_files:
        exit("No Files Found")

    # Create the output folder if it doesn't exist
    if not os.path.exists(OutDir):
        os.makedirs(OutDir)

    # Limit the number of concurrent threads to 3
    semaphore = threading.Semaphore(3)

    # Iterate through the excel files
    for input_file in input_files:

        def _thread(input_file):
            with semaphore:
                try:
                    # Convert the excel file to csv
                    output_file = f"{OutDir}\\{input_file.removesuffix('.xlsx')}.csv"
                    csv_data = convert_excel_to_csv(
                        f"{InDir}\\{input_file}", output_file
                    )

                    # Initialize the data array
                    DATA = []

                    # Split the csv data into lines
                    lines = csv_data.splitlines()

                    # Iterate through the lines
                    for line in lines:

                        # Split the line into cells
                        data = line.split(",")

                        # Append the cells to the data array, while removing the first 3 cells (because they are created by the converter as indexes)
                        DATA.append(data[3:])

                    # Remove lines that are full of commas at the end of the file
                    while DATA and all(not cell.strip() for cell in DATA[-1]):
                        DATA.pop()

                    # Add a line of commas at the start of the data array, for proper indexing
                    DATA.insert(0, [","] * len(DATA[0]))

                    # Add the data to the list
                    DATALIST.append([input_file, DATA])
                except Exception as e:
                    print(f"Error processing {input_file}: {e}")
                    Thread(target=_thread, args=(input_file,)).start()

        # Start the thread
        sleep(0.5)
        Thread(target=_thread, args=(input_file,)).start()

    for thread in threading.enumerate():
        if thread is not threading.current_thread():
            thread.join()

    # Wait for the batch file to finish, then delete it
    if os.path.exists("convert.bat"):
        os.remove("convert.bat")

    # Initialize the XML string
    XML = Definitions.Base_XML_Start

    for input_file, DATA in DATALIST:
        # Initialize the list of active planets
        PLANET_INDEXES = []

        # Get the star mass
        try:
            star_mass = float(
                DATA[letter_to_int(Definitions.Star_Mass.split(":")[0])][
                    int(Definitions.Star_Mass.split(":")[1])
                ]
            )
        except ValueError:
            star_mass = 0
        # Get the surface temperature
        try:
            surface_temperature = float(
                DATA[letter_to_int(Definitions.Surface_Temperature.split(":")[0])][
                    int(Definitions.Surface_Temperature.split(":")[1])
                ]
            )
        except ValueError:
            surface_temperature = 0
        # Get the luminosity
        try:
            luminosity = float(
                DATA[letter_to_int(Definitions.Luminosity.split(":")[0])][
                    int(Definitions.Luminosity.split(":")[1])
                ]
            )
        except ValueError:
            luminosity = 0
        # Get the radius
        try:
            radius = float(
                DATA[letter_to_int(Definitions.Radius.split(":")[0])][
                    int(Definitions.Radius.split(":")[1])
                ]
            )
        except ValueError:
            radius = 0
        # Get the system age
        try:
            system_age = float(
                DATA[letter_to_int(Definitions.System_Age.split(":")[0])][
                    int(Definitions.System_Age.split(":")[1])
                ]
            )
        except ValueError:
            system_age = 0
        # Generate a random color for the star, a tuple with a maximum of 255 that always adds up to 300
        star_color = [random.randint(0, 255) for _ in range(3)]
        color_sum = sum(star_color)
        star_color = [int((value / color_sum) * 255) for value in star_color]

        # Add the star to the XML string
        XML += f"""
            <location type="StarSystem" name="System-{random.randint(0,10000)}" faction="" pedia=""
                position="{random.randint(10, 10000)/100} {random.randint(10, 10000)/100} {random.randint(10, 10000)/100}"
                color="{' '.join(map(str, star_color))} 255" ambient="255 255 255 255">
        """

        # Iterate through the planets to find which ones have values entered
        for i in range(Definitions.Planet_Start_Row, Definitions.Planet_End_Max_Row):

            # Get the planet data
            try:
                planet_data = DATA[i][letter_to_int(Definitions.Mass_Col)]
            except ValueError:
                planet_data = 0
            except IndexError:
                try:
                    DATA[i]
                    try:
                        DATA[i][letter_to_int(Definitions.Mass_Col)]
                    except IndexError:
                        print(
                            f"IndexError at row {i}, col {letter_to_int(Definitions.Mass_Col)}, line 325"
                        )
                        exit()
                except IndexError:
                    print(f"IndexError at row {i}, line 325")
                    exit()
            # If the planet data is not empty, add it to the active planets
            if planet_data:
                PLANET_INDEXES.append(i)

        # Iterate through the active planets
        for i in PLANET_INDEXES:

            # Get the planet data
            planet_data = DATA[i]

            # Get the planet name
            planet_name = planet_data[letter_to_int(Definitions.Suffix_Col)]

            # Get the planet mass
            try:
                planet_mass = float(planet_data[letter_to_int(Definitions.Mass_Col)])
            except ValueError:
                planet_mass = 0

            # Get the planet radius
            try:
                planet_radius = float(
                    planet_data[letter_to_int(Definitions.Radius_Col)]
                )
            except ValueError:
                planet_radius = 0

            # Get the planet semimajor axis
            try:
                planet_semimajor_axis = float(
                    planet_data[letter_to_int(Definitions.Semimajor_Axis_Col)]
                )
            except ValueError:
                planet_semimajor_axis = 0

            # Get the planet period days
            try:
                planet_period_days = float(
                    planet_data[letter_to_int(Definitions.Period_Days_Col)]
                )
            except ValueError:
                planet_period_days = 0

            # Get the planet eccentricity
            try:
                planet_eccentricity = float(
                    planet_data[letter_to_int(Definitions.Eccentricity_Col)]
                )
            except ValueError:
                planet_eccentricity = 0

            # Get the habitable zone
            try:
                habitable_zone = float(
                    planet_data[letter_to_int(Definitions.Habitable_Zone_Col)]
                )
            except ValueError:
                habitable_zone = 0

            # Get the tectonic habitability
            try:
                tectonic_habitability = float(
                    planet_data[letter_to_int(Definitions.Tectonic_Habitability_Col)]
                )
            except ValueError:
                tectonic_habitability = 0

            # Get the rotation period
            try:
                rotation_period = float(
                    planet_data[letter_to_int(Definitions.Rotation_Period_Col)]
                )
            except ValueError:
                rotation_period = 0

            # Generate a random color for the planet, a tuple with a maximum of 255 that always adds up to 300
            planet_color = [random.randint(0, 255) for _ in range(3)]
            color_sum = sum(planet_color)
            planet_color = [int((value / color_sum) * 255) for value in planet_color]

            # Add the planet to the XML string
            XML += f"""
                <planet weather="" color="{' '.join(map(str, planet_color))} 255" orbitaldistance="{planet_semimajor_axis}"
                    orbitalposition="{random.randint(0, 360)}" orbitalperiod="{planet_period_days /360}"
                    rotationperiod="{rotation_period}" mass="{planet_mass}" radius="{planet_radius * 6371}"
                    density="5.43" axistilt="{random.randint(1, 400)/10}" name="{planet_name}">
                    <description />
                    <pedia />
                </planet>
"""
        # Add the end of the star system
        XML += """
            </location>
"""

    # Add the end of the XML string
    XML += Definitions.Base_XML_End

    # Write the XML string to a file
    with open(f"{OutDir}\\MASTER.xml", "w") as f:
        f.write(XML)

    print(f"XML file has been created successfully at file://{OutDir}/MASTER.xml")
    cleanup(OutDir)


run(InDir=filedialog.askdirectory(), OutDir=filedialog.askdirectory())
