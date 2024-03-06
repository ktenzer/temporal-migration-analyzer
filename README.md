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

`
filename,workflowid,signals,is update,child workflows,is child,input search attributes,search attribute upserts,migration recommendation

82b083e3-7e17-4fcf-9922-9926d77bbde8_events.json,order-317711,0,False,0,False,False,5,drainable
1ff81ed3-1d6a-40ad-a5e3-c94af8c371c4_events.json,order-153996,0,False,3,False,False,0,custom
d296b6ae-6b50-49dc-a231-99aa9695b1e8_events.json,order-148643,0,True,0,False,False,0,custom
three_signal_events.json,TRANSFER-VSV-155,3,False,0,False,False,0,custom
f235c3c9-0b5d-4d72-b97c-46fd1cc656c6_events.json,shipment-153996-654321,0,False,0,True,False,0,custom
zero_signal_events.json,TRANSFER-SOQ-104,0,False,0,False,False,0,drainable
one_signal_events.json,TRANSFER-BAX-210,1,False,0,False,False,0,custom
`
