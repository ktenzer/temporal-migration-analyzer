## Temporal Migration Analyzer
Thanks to colleague [Steve Adroulakis](https://github.com/steveandroulakis) for providing inspiration and example for parsing Temporal Workflow history.

This python script will take a directory containing one or more Temporal Workflow histories and analyze each to recommend migration approach. It will also point out things that should be considered when migrating a workflow from one namespace to another (typically between self-hosted and cloud). 

It will point out if a workflow is a child, start children, recieves a signal, recieves a update or uses search attributes.

Output is forvided in csv format so it can be imported into excel.

## Instructions
`$ python migration_advisor.py <Directory of JSON History Files>`

To run on example history files:

`$ python migration_advisor.py example_history`

Output:

|filename|workflowid|isLongRunning|isContinueAsNew|isSignal|isUpdate|isParent|isChild|isInputSearchAttribute|isUpsertSearchAttributes|recommendation|
|search_attributes_events.json|order-317711|False|False|False|False|False|False|False|True|drainable|
