## Temporal Migration Analyzer
Thanks to colleague [Steve Adroulakis](https://github.com/steveandroulakis) for providing inspiration and example for parsing Temporal Workflow history.

This python script will take a directory containing one or more Temporal Workflow histories and analyze each to recommend migration approach. It will also point out things that should be considered when migrating a workflow from one namespace to another (typically between self-hosted and cloud). 

It will point out if a workflow is a child, start children, recieves a signal, recieves a update or uses search attributes.

Output is forvided in csv format so it can be imported into excel.

## Instructions
`$ python migration_advisor.py <Directory of JSON History Files>`

To run on example history files:

`$ python migration_advisor.py example_history`

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

Output:

| filename | workflowid | isLongRunning | isContinueAsNew | isSignal | isUpdate | isParent |isChild | isInputSearchAttribute |isUpsertSearchAttributes | recommendation |
| search_attributes_events.json | order-317711 | False | False | False | False | False | False |False | True | drainable |
|update_events.json,order-148643,False|False|False|True|False|False|False|False|custom|
|parent_events.json,order-153996|False|False|False|False|True|False|False|False|custom|
|three_signal_events.json|TRANSFER-VSV-155|False|False|True|False|False|False|False|False|custom|
|zero_signal_events.json|TRANSFER-SOQ-104|False|False|False|False|False|False|False|False|drainable|
|one_signal_events.json|TRANSFER-BAX-210|False|False|True|False|False|False|False|False|custom|
|child_events.json,shipment-153996-654321,False,False,False,False,False,True,False,False,custom|
|continue-as-new_events.json|child_workflow:c4efae11-7b91-4c53-ac6c-64abb4ff70f7|False|True|False|False|False|True|False|False|custom|
