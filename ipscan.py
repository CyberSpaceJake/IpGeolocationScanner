import ipinfo
import re
import ipaddress
import csv
import os

def is_valid_ip(ip):
    # Regular expression to validate IP address format
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return ip_pattern.match(ip) is not None

def is_private_ip(ip):
    # Convert the string IP address to an ipaddress object
    ip_obj = ipaddress.ip_address(ip)
    return ip_obj.is_private

def get_valid_ip():
    while True:
        # Ask the user for an IP address
        ip = input("Please enter an IP address: ")

        # Validate IP address format
        if not is_valid_ip(ip):
            print("Error: Invalid IP address format. Please enter a valid IP address.")
            continue

        # Check if the IP address is within a private range
        if is_private_ip(ip):
            print("Error: The IP address is within a private IP range. Please enter a public IP address.")
            continue

        return ip

def save_to_csv(ip_details_list):
    while True:
        # Ask the user for the filename
        filename = input("Enter the filename for the CSV (e.g., output.csv): ").strip()
        
        # Check if the file already exists
        if os.path.exists(filename):
            print(f"Error: The file '{filename}' already exists. Please choose a different name.")
            continue  # Automatically ask for a new filename
        
        # Define CSV fieldnames, excluding "country_flag"
        fieldnames = [key for key in ip_details_list[0].keys() if key != 'country_flag']

        # Write the IP details to a CSV file with UTF-8 encoding
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for details in ip_details_list:
                # Exclude "country_flag" from the details before writing to CSV
                filtered_details = {key: value for key, value in details.items() if key != 'country_flag'}
                writer.writerow(filtered_details)
        
        # Get the absolute path of the saved file
        file_path = os.path.abspath(filename)
        print(f"Information successfully saved to {file_path}.")
        break  # Exit the loop after successfully saving the file

def main():
    # Access token for ipinfo
    token = 'REPLACE_THIS'
    handler = ipinfo.getHandler(token)
    ip_details_list = []

    while True:
        # Get a valid public IP address from the user
        ip = get_valid_ip()

        # Gather IP information
        details = handler.getDetails(ip)

        # Print all details, excluding "country_flag"
        for key, value in details.all.items():
            if key != 'country_flag':
                print(f'{key}: {value}')
        
        # Store the details in a dictionary, excluding "country_flag"
        ip_details = {key: value for key, value in details.all.items() if key != 'country_flag'}
        ip_details_list.append(ip_details)

        # Check if the IP address is outside the US
        if details.country != 'US':
            print("\nWarning: This IP address is outside the US.")
            print("Consider further investigation and possible blocking on the firewall.")
        else:
            print("\nThis IP address is within the US.")

        # Ask if the user wants to enter another IP
        again = input("\nWould you like to enter another IP address? (Y/N): ").strip().lower()
        if again != 'y':
            # Ask if the user wants to save the information to a CSV file
            save = input("Would you like to save the information to a CSV file? (Y/N): ").strip().lower()
            if save == 'y':
                save_to_csv(ip_details_list)
            print("Exiting the script.")
            break
    
    # Prevent the terminal from closing immediately
    input("\nPress Enter to exit and close the terminal.")

if __name__ == "__main__":
    main()
