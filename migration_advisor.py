import json
import csv
import sys
from pathlib import Path

def analyze_history(filepath):
    """
    Count the 'WorkflowExecutionSignaled' events and extract workflow ID from a JSON file.
    Handle JSON errors and missing keys gracefully.
    """
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {filepath}")
        return None, 0

    workflow_id = data.get('events', [{}])[0].get('workflowExecutionStartedEventAttributes', {}).get('workflowId', 'Unknown')
    signal_count = sum(1 for event in data.get('events', []) if event.get('eventType') == "WorkflowExecutionSignaled")
    child_workflow_count = sum(1 for event in data.get('events', []) if event.get('eventType') == "ChildWorkflowExecutionStarted")
    search_attribute_upsert_count = sum(1 for event in data.get('events', []) if event.get('eventType') == "UpsertWorkflowSearchAttributes")
    parent_workflow = data.get('events', [{}])[0].get('workflowExecutionStartedEventAttributes', {}).get('parentWorkflowExecution', 'Unknown')
    search_attributes_input = data.get('events', [{}])[0].get('workflowExecutionStartedEventAttributes', {}).get('searchAttributes', 'Unknown')
    update_accepted = sum(1 for event in data.get('events', []) if event.get('eventType') == "WorkflowExecutionUpdateAccepted")
    update_rejected = sum(1 for event in data.get('events', []) if event.get('eventType') == "WorkflowExecutionUpdateRejected")

    isChildWorkflow = False
    if parent_workflow != None:
        isChildWorkflow = True

    isSearchAttributeInput = False
    if search_attributes_input != None:
        isSearchAttributeInput = True

    isUpdate = False
    if update_accepted > 0 or update_rejected > 0:
        isUpdate = True

    return workflow_id, signal_count, isUpdate, child_workflow_count, isChildWorkflow, isSearchAttributeInput, search_attribute_upsert_count

def process_directory(directory):
    """
    Process all JSON files in the given directory and return the counts.
    Uses Path.glob for efficient file filtering.
    """
    directory_path = Path(directory)
    results = []
    for file_path in directory_path.glob('*.json'):
        workflow_id, signal_count, isUpdate, child_workflow_count, isChildWorkflow, isSearchAttributeInput, search_attribute_upsert_count = analyze_history(file_path)

        migration_recommendation = ''
        if signal_count > 0 or child_workflow_count > 0 or isChildWorkflow or isUpdate:
            migration_recommendation = 'custom'
        else:
            migration_recommendation = 'drainable'

        if workflow_id:
            results.append((file_path.name, workflow_id, signal_count, isUpdate, child_workflow_count, isChildWorkflow, isSearchAttributeInput, search_attribute_upsert_count, migration_recommendation))
    return results

def output_to_stdout(results):
    """
    Output the results to stdout in CSV format.
    """
    writer = csv.writer(sys.stdout)
    writer.writerow(['filename', 'workflowid', 'signals', 'is update', 'child workflows', 'is child', 'input search attributes', 'search attribute upserts', 'migration recommendation'])
    writer.writerows(results)

def main():
    if len(sys.argv) < 2:
        print("Usage: python count_signals.py <Directory of History Files>")
        sys.exit(1)

    directory = sys.argv[1]
    if not Path(directory).is_dir():
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    results = process_directory(directory)
    output_to_stdout(results)

if __name__ == "__main__":
    main()
