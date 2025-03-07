import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import TipMoreInfoOnRegex from '../components/_tip_more_info_on_regex.mdx'
import ConfigForAssetsConfiguredSingle from '../filesystem_components/_config_for_assets_configured_single.mdx'
import NoteExplicitConfiguredAssetsSingle from '../filesystem_components/_note_explicit_configured_assets_single.mdx'
import ConfigForAssetsConfiguredMulti from '../filesystem_components/_config_for_assets_configured_multi.mdx'
import NoteExplicitConfiguredAssetsMulti from '../filesystem_components/_note_explicit_configured_assets_multi.mdx'

<Tabs
  groupId="batch-count"
  defaultValue='single'
  values={[
  {label: 'Single Batch Configuration', value:'single'},
  {label: 'Multi-Batch Configuration', value:'multi'},
  ]}>
    
  <TabItem value="single">

<ConfigForAssetsConfiguredSingle />

And the full configuration for your Datasource should look like:

```python
datasource_config = {
    "name": "my_datasource_name",
    "class_name": "Datasource",
    "module_name": "great_expectations.datasource",
    "execution_engine": {
        "class_name": "PandasExecutionEngine",  
        "module_name": "great_expectations.execution_engine",
    },
    "data_connectors": {
        "name_of_my_configured_data_connector": {
            "class_name": "ConfiguredAssetFilesystemDataConnector",
            "base_directory": "../data",
            "assets": {
                "yellow_tripdata_jan": {
                  "pattern": "yellow_tripdata_sample_2020-(01)\\.csv",
                  "group_names": ["month"],
                }
            }
        }
    }
}
```

<NoteExplicitConfiguredAssetsSingle />

  </TabItem>
  <TabItem value="multi">


<ConfigForAssetsConfiguredMulti />

And the full configuration for your Datasource should look like:

```python
datasource_config = {
    "name": "my_datasource_name",
    "class_name": "Datasource",
    "module_name": "great_expectations.datasource",
    "execution_engine": {
        "class_name": "PandasExecutionEngine",  
        "module_name": "great_expectations.execution_engine",
    },
    "data_connectors": {
        "name_of_my_configured_data_connector": {
            "class_name": "ConfiguredAssetFilesystemDataConnector",
            "base_directory": "../data",
            "assets": {
                "yellow_tripdata_jan": {
                  "pattern": "yellow_tripdata_sample_2020-(.*)\\.csv",
                  "group_names": ["month"],
                }
            }
        }
    }
}
```

<NoteExplicitConfiguredAssetsMulti />

  </TabItem>
  </Tabs>