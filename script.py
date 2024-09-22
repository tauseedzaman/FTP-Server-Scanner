import ftplib
import csv

# Read the list of hosts from the text file
with open('hosts.txt', 'r') as f:
    hosts = [line.strip() for line in f.readlines()]

# Create a CSV file to store the output
with open('ftp_output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Host', 'Name'])

    # Iterate over the hosts
    for host in hosts:
        try:
            # Connect to the FTP server (optional: set a timeout)
            ftp = ftplib.FTP()
            ftp.connect(host, timeout=10)
            ftp.login()  # Defaults to anonymous login

            # Define a recursive function to list files and folders
            def list_files(ftp, path, writer):
                try:
                    # List the contents of the current directory
                    contents = ftp.nlst(path)
                    for item in contents:
                        # Get the full path of the item
                        full_path = f"{path}/{item}"
                        # Check if the item is a directory
                        try:
                            ftp.cwd(full_path)
                            # If it's a directory, recursively list its contents
                            list_files(ftp, full_path, writer)
                            ftp.cwd('..')  # Go back to the parent directory
                        except ftplib.error_perm:
                            # If it's not a directory, write it to the CSV file
                            writer.writerow([host,item])
                except Exception as e:
                    writer.writerow([host, f"Error: {str(e)}"])

            # Start the recursion from the root directory
            list_files(ftp, '', writer)

        except ftplib.all_errors as e:
            print(f"Error connecting to {host}: {e}")
            writer.writerow([host, '', f"Error: {str(e)}"])
        finally:
            try:
                ftp.quit()
            except:
                pass