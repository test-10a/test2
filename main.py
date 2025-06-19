import argparse
from compliance_suite.certifier import perform_certification

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enterprise Security Compliance Suite')
    parser.add_argument('command', choices=['validate', 'certify'])
    parser.add_argument('--level', type=int, default=3)
    parser.add_argument('--output', default='audit_report.json')
    
    args = parser.parse_args()
    
    if args.command == 'validate':
        from compliance_suite.validator import validate_environment
        status = validate_environment()
        print("Validation result:", "SUCCESS" if status else "FAILURE")
        exit(0 if status else 1)
        
    elif args.command == 'certify':
        success = perform_certification(args.output)
        exit(0 if success else 1)
