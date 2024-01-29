import subprocess

try:
    # Execute the command to get the list of profiles
    result = subprocess.check_output("cmd /c netsh wlan show profiles", stderr=subprocess.STDOUT, text=True)

    # Split the result into lines
    lines = result.splitlines()

    # Initialize a dictionary to hold SSID names and their key content
    ssid_key_dict = {}

    # Loop through each line in the output
    for line in lines:
        # Check if the line contains an SSID
        if "All User Profile" in line:
            # Extract the SSID name, which comes after the colon and strip any whitespace
            ssid = line.split(":")[1].strip()

            # Execute the command to get the key content for the SSID
            key_result = subprocess.check_output(
                f"cmd /c netsh wlan show profile name=\"{ssid}\" key=clear",
                stderr=subprocess.STDOUT, text=True
            )

            # Split the key result into lines
            key_lines = key_result.splitlines()

            # Loop through each line in the key result
            for key_line in key_lines:
                # Check if the line contains the key content
                if "Key Content" in key_line:
                    # Extract the key content, which comes after the colon and strip any whitespace
                    key_content = key_line.split(":")[1].strip()
                    ssid_key_dict[ssid] = key_content

    # Determine the maximum width for the SSID
    max_ssid_width = max(len(ssid) for ssid in ssid_key_dict.keys())

    # Save the SSID names and their key content to a file with ":" aligned in the same column
    with open("wifi_info.txt", "w") as f:
        for ssid, key_content in ssid_key_dict.items():
            # Format the output with a fixed width for SSID
            formatted_line = f"{ssid.ljust(max_ssid_width)} : {key_content}\n"
            f.write(formatted_line)
    
except subprocess.CalledProcessError as e:
    print("Error:", e)
