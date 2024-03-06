import json
import csv
import sys
from pathlib import Path
from datetime import datetime
from datetime import timezone

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

    events = len(data['events'])
    start_time = data['events'][0]['eventTime']
    end_time = data['events'][events - 1]['eventTime']

    convert_start_time = datetime.fromisoformat(start_time[:-1]).astimezone(timezone.utc)
    convert_end_time = datetime.fromisoformat(end_time[:-1]).astimezone(timezone.utc)
    start_time_epoch = convert_start_time.timestamp()
    end_time_epoch = convert_end_time.timestamp()

    isLongRunning = False
    if end_time_epoch - start_time_epoch > 86400:
        isLongRunning = True

    workflow_id = data.get('events', [{}])[0].get('workflowExecutionStartedEventAttributes', {}).get('workflowId', 'Unknown')
    isSignal = any(1 for event in data.get('events', []) if event.get('eventType') == "WorkflowExecutionSignaled")
    isParentWorkflow = any(1 for event in data.get('events', []) if event.get('eventType') == "ChildWorkflowExecutionStarted")
    isUpsertSearchAttributes = any(1 for event in data.get('events', []) if event.get('eventType') == "UpsertWorkflowSearchAttributes")
    parent_workflow = data.get('events', [{}])[0].get('workflowExecutionStartedEventAttributes', {}).get('parentWorkflowExecution', 'Unknown')
    search_attributes_input = data.get('events', [{}])[0].get('workflowExecutionStartedEventAttributes', {}).get('searchAttributes', 'Unknown')
    isUpdateAccepted = any(1 for event in data.get('events', []) if event.get('eventType') == "WorkflowExecutionUpdateAccepted")
    isUpdateRejected = any(1 for event in data.get('events', []) if event.get('eventType') == "WorkflowExecutionUpdateRejected")
    isContinueAsNew = any(1 for event in data.get('events', []) if event.get('eventType') == "WorkflowExecutionContinuedAsNew")



    isChildWorkflow = False
    if parent_workflow != None:
        isChildWorkflow = True

    isSearchAttributeInput = False
    if search_attributes_input != None:
        isSearchAttributeInput = True

    isUpdate = False
    if isUpdateAccepted or isUpdateRejected:
        isUpdate = True

    return workflow_id, isLongRunning, isContinueAsNew, isSignal, isUpdate, isParentWorkflow, isChildWorkflow, isSearchAttributeInput, isUpsertSearchAttributes

def process_directory(directory):
    """
    Process all JSON files in the given directory and return the counts.
    Uses Path.glob for efficient file filtering.
    """
    directory_path = Path(directory)
    results = []
    for file_path in directory_path.glob('*.json'):
        workflow_id, isLongRunning, isContinueAsNew, isSignal, isUpdate, isParentWorkflow, isChildWorkflow, isSearchAttributeInput, isUpsertSearchAttributes = analyze_history(file_path)

        migration_recommendation = ''
        if isSignal or isParentWorkflow or isChildWorkflow or isUpdate or isLongRunning:
            migration_recommendation = 'custom'
        else:
            migration_recommendation = 'drainable'

        if workflow_id:
            results.append((file_path.name, workflow_id, isLongRunning, isContinueAsNew, isSignal, isUpdate, isParentWorkflow, isChildWorkflow, isSearchAttributeInput, isUpsertSearchAttributes, migration_recommendation))
    return results

def output_to_stdout(results):
    """
    Output the results to stdout in CSV format.
    """
    writer = csv.writer(sys.stdout)
    writer.writerow(['filename', 'workflowid', 'isLongRunning', 'isContinueAsNew', 'isSignal', 'isUpdate', 'isParent', 'isChild', 'isInputSearchAttribute', 'isUpsertSearchAttributes', 'recommendation'])
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
