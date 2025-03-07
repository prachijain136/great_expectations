import json
from copy import deepcopy
from string import Template as pTemplate
from typing import List, Optional

from marshmallow import INCLUDE, Schema, fields, post_dump, post_load

from great_expectations.render.exceptions import InvalidRenderedContentError
from great_expectations.types import DictDot


class RenderedContent:
    def to_json_dict(self):
        return {}

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            # Delegate comparison to the other instance's __eq__.
            return NotImplemented
        return self.to_json_dict() == other.to_json_dict()

    @classmethod
    def rendered_content_list_to_json(cls, list_, check_dicts=False):
        result_list = []
        for item in list_:
            if isinstance(item, RenderedContent):
                result_list.append(item.to_json_dict())
            elif isinstance(item, list):
                result_list.append(
                    RenderedContent.rendered_content_list_to_json(
                        item, check_dicts=check_dicts
                    )
                )
            elif check_dicts and isinstance(item, dict):
                result_list.append(cls.rendered_content_dict_to_json(item))
            else:
                result_list.append(item)
        return result_list

    @classmethod
    def rendered_content_dict_to_json(cls, dict_, check_list_dicts=True):
        json_dict = deepcopy(dict_)
        for key, val in json_dict.items():
            if not isinstance(val, (RenderedContent, list, dict)):
                continue
            elif isinstance(val, RenderedContent):
                json_dict[key] = val.to_json_dict()
            elif isinstance(val, list):
                json_dict[key] = cls.rendered_content_list_to_json(
                    val, check_list_dicts
                )
            elif isinstance(val, dict):
                json_dict[key] = cls.rendered_content_dict_to_json(
                    val, check_list_dicts
                )
        return json_dict


class RenderedComponentContent(RenderedContent):
    def __init__(self, content_block_type, styling=None) -> None:
        self.content_block_type = content_block_type
        if styling is None:
            styling = {}
        self.styling = styling

    def to_json_dict(self):
        d = super().to_json_dict()
        d["content_block_type"] = self.content_block_type
        if len(self.styling) > 0:
            d["styling"] = self.styling
        return d


class RenderedHeaderContent(RenderedComponentContent):
    def __init__(
        self,
        header,
        subheader=None,
        header_row=None,
        styling=None,
        content_block_type="header",
    ) -> None:
        super().__init__(content_block_type=content_block_type, styling=styling)
        self.header = header
        self.header_row = header_row
        self.subheader = subheader

    def to_json_dict(self):
        d = super().to_json_dict()
        if isinstance(self.header, RenderedContent):
            d["header"] = self.header.to_json_dict()
        else:
            d["header"] = self.header
        if self.subheader is not None:
            if isinstance(self.subheader, RenderedContent):
                d["subheader"] = self.subheader.to_json_dict()
            else:
                d["subheader"] = self.subheader
        if self.header_row:
            d["header_row"] = self.header_row
        return d


class RenderedGraphContent(RenderedComponentContent):
    def __init__(
        self,
        graph,
        header=None,
        subheader=None,
        styling=None,
        content_block_type="graph",
    ) -> None:
        super().__init__(content_block_type=content_block_type, styling=styling)
        self.graph = graph
        self.header = header
        self.subheader = subheader

    def to_json_dict(self):
        d = super().to_json_dict()
        d["graph"] = self.graph
        if self.header is not None:
            if isinstance(self.header, RenderedContent):
                d["header"] = self.header.to_json_dict()
            else:
                d["header"] = self.header
        if self.subheader is not None:
            if isinstance(self.subheader, RenderedContent):
                d["subheader"] = self.subheader.to_json_dict()
            else:
                d["subheader"] = self.subheader
        return d


class RenderedTableContent(RenderedComponentContent):
    def __init__(
        self,
        table,
        header=None,
        subheader=None,
        header_row=None,
        styling=None,
        content_block_type="table",
        table_options=None,
        header_row_options=None,
    ) -> None:
        super().__init__(content_block_type=content_block_type, styling=styling)
        self.header = header
        self.subheader = subheader
        self.table = table
        self.table_options = table_options
        self.header_row = header_row
        self.header_row_options = header_row_options

    def to_json_dict(self):
        d = super().to_json_dict()
        if self.header is not None:
            if isinstance(self.header, RenderedContent):
                d["header"] = self.header.to_json_dict()
            else:
                d["header"] = self.header
        if self.subheader is not None:
            if isinstance(self.subheader, RenderedContent):
                d["subheader"] = self.subheader.to_json_dict()
            else:
                d["subheader"] = self.subheader
        d["table"] = RenderedContent.rendered_content_list_to_json(self.table)
        if self.header_row is not None:
            d["header_row"] = RenderedContent.rendered_content_list_to_json(
                self.header_row
            )
        if self.header_row_options is not None:
            d["header_row_options"] = self.header_row_options
        if self.table_options is not None:
            d["table_options"] = self.table_options
        return d


class RenderedTabsContent(RenderedComponentContent):
    def __init__(
        self, tabs, header=None, subheader=None, styling=None, content_block_type="tabs"
    ) -> None:
        super().__init__(content_block_type=content_block_type, styling=styling)
        self.tabs = tabs
        self.header = header
        self.subheader = subheader

    def to_json_dict(self):
        d = super().to_json_dict()
        d["tabs"] = RenderedContent.rendered_content_list_to_json(
            self.tabs, check_dicts=True
        )
        if self.header is not None:
            if isinstance(self.header, RenderedContent):
                d["header"] = self.header.to_json_dict()
            else:
                d["header"] = self.header
        if self.subheader is not None:
            if isinstance(self.subheader, RenderedContent):
                d["subheader"] = self.subheader.to_json_dict()
            else:
                d["subheader"] = self.subheader
        return d


class RenderedBootstrapTableContent(RenderedComponentContent):
    def __init__(
        self,
        table_data,
        table_columns,
        title_row=None,
        table_options=None,
        header=None,
        subheader=None,
        styling=None,
        content_block_type="bootstrap_table",
    ) -> None:
        super().__init__(content_block_type=content_block_type, styling=styling)
        self.table_data = table_data
        self.table_columns = table_columns
        self.title_row = title_row
        self.table_options = table_options
        self.header = header
        self.subheader = subheader

    def to_json_dict(self):
        d = super().to_json_dict()
        d["table_data"] = RenderedContent.rendered_content_list_to_json(
            self.table_data, check_dicts=True
        )
        d["table_columns"] = RenderedContent.rendered_content_list_to_json(
            self.table_columns, check_dicts=True
        )
        if self.table_options is not None:
            d["table_options"] = self.table_options
        if self.title_row is not None:
            if isinstance(self.title_row, RenderedContent):
                d["title_row"] = self.title_row.to_json_dict()
            else:
                d["title_row"] = self.title_row
        if self.header is not None:
            if isinstance(self.header, RenderedContent):
                d["header"] = self.header.to_json_dict()
            else:
                d["header"] = self.header
        if self.subheader is not None:
            if isinstance(self.subheader, RenderedContent):
                d["subheader"] = self.subheader.to_json_dict()
            else:
                d["subheader"] = self.subheader
        return d


class RenderedContentBlockContainer(RenderedComponentContent):
    def __init__(
        self, content_blocks, styling=None, content_block_type="content_block_container"
    ) -> None:
        super().__init__(content_block_type=content_block_type, styling=styling)
        self.content_blocks = content_blocks

    def to_json_dict(self):
        d = super().to_json_dict()
        d["content_blocks"] = RenderedContent.rendered_content_list_to_json(
            self.content_blocks
        )
        return d


class RenderedMarkdownContent(RenderedComponentContent):
    def __init__(self, markdown, styling=None, content_block_type="markdown") -> None:
        super().__init__(content_block_type=content_block_type, styling=styling)
        self.markdown = markdown

    def to_json_dict(self):
        d = super().to_json_dict()
        d["markdown"] = self.markdown
        return d


class RenderedStringTemplateContent(RenderedComponentContent):
    def __init__(
        self, string_template, styling=None, content_block_type="string_template"
    ) -> None:
        super().__init__(content_block_type=content_block_type, styling=styling)
        self.string_template = string_template

    def to_json_dict(self):
        d = super().to_json_dict()
        d["string_template"] = self.string_template
        return d

    def __str__(self):
        string = pTemplate(self.string_template["template"]).safe_substitute(
            self.string_template["params"]
        )
        return string

    def __eq__(self, other):
        return str(self) == str(other)


class RenderedBulletListContent(RenderedComponentContent):
    def __init__(
        self,
        bullet_list,
        header=None,
        subheader=None,
        styling=None,
        content_block_type="bullet_list",
    ) -> None:
        super().__init__(content_block_type=content_block_type, styling=styling)
        self.header = header
        self.subheader = subheader
        self.bullet_list = bullet_list

    def to_json_dict(self):
        d = super().to_json_dict()
        d["bullet_list"] = RenderedContent.rendered_content_list_to_json(
            self.bullet_list
        )
        if self.header is not None:
            if isinstance(self.header, RenderedContent):
                d["header"] = self.header.to_json_dict()
            else:
                d["header"] = self.header
        if self.subheader is not None:
            if isinstance(self.subheader, RenderedContent):
                d["subheader"] = self.subheader.to_json_dict()
            else:
                d["subheader"] = self.subheader
        return d


class ValueListContent(RenderedComponentContent):
    def __init__(
        self,
        value_list,
        header=None,
        subheader=None,
        styling=None,
        content_block_type="value_list",
    ) -> None:
        super().__init__(content_block_type=content_block_type, styling=styling)
        self.header = header
        self.subheader = subheader
        self.value_list = value_list

    def to_json_dict(self):
        d = super().to_json_dict()
        if self.header is not None:
            if isinstance(self.header, RenderedContent):
                d["header"] = self.header.to_json_dict()
            else:
                d["header"] = self.header
        if self.subheader is not None:
            if isinstance(self.subheader, RenderedContent):
                d["subheader"] = self.subheader.to_json_dict()
            else:
                d["subheader"] = self.subheader
        d["value_list"] = RenderedContent.rendered_content_list_to_json(self.value_list)
        return d


class TextContent(RenderedComponentContent):
    def __init__(
        self, text, header=None, subheader=None, styling=None, content_block_type="text"
    ) -> None:
        super().__init__(content_block_type=content_block_type, styling=styling)
        self.text = text
        self.header = header
        self.subheader = subheader

    def to_json_dict(self):
        d = super().to_json_dict()
        if self.header is not None:
            if isinstance(self.header, RenderedContent):
                d["header"] = self.header.to_json_dict()
            else:
                d["header"] = self.header
        if self.subheader is not None:
            if isinstance(self.subheader, RenderedContent):
                d["subheader"] = self.subheader.to_json_dict()
            else:
                d["subheader"] = self.subheader
        d["text"] = RenderedContent.rendered_content_list_to_json(self.text)

        return d


class CollapseContent(RenderedComponentContent):
    def __init__(
        self,
        collapse,
        collapse_toggle_link=None,
        header=None,
        subheader=None,
        styling=None,
        content_block_type="collapse",
        inline_link=False,
    ) -> None:
        super().__init__(content_block_type=content_block_type, styling=styling)
        self.collapse_toggle_link = collapse_toggle_link
        self.header = header
        self.subheader = subheader
        self.collapse = collapse
        self.inline_link = inline_link

    def to_json_dict(self):
        d = super().to_json_dict()
        if self.header is not None:
            if isinstance(self.header, RenderedContent):
                d["header"] = self.header.to_json_dict()
            else:
                d["header"] = self.header
        if self.subheader is not None:
            if isinstance(self.subheader, RenderedContent):
                d["subheader"] = self.subheader.to_json_dict()
            else:
                d["subheader"] = self.subheader
        if self.collapse_toggle_link is not None:
            if isinstance(self.collapse_toggle_link, RenderedContent):
                d["collapse_toggle_link"] = self.collapse_toggle_link.to_json_dict()
            else:
                d["collapse_toggle_link"] = self.collapse_toggle_link
        d["collapse"] = RenderedContent.rendered_content_list_to_json(self.collapse)
        d["inline_link"] = self.inline_link

        return d


class RenderedDocumentContent(RenderedContent):
    # NOTE: JPC 20191028 - review these keys to consolidate and group
    def __init__(
        self,
        sections,
        data_asset_name=None,
        full_data_asset_identifier=None,
        renderer_type=None,
        page_title=None,
        utm_medium=None,
        cta_footer=None,
        expectation_suite_name=None,
        batch_kwargs=None,
        batch_spec=None,
        ge_cloud_id=None,
    ) -> None:
        if not isinstance(sections, list) and all(
            [isinstance(section, RenderedSectionContent) for section in sections]
        ):
            raise InvalidRenderedContentError(
                "RenderedDocumentContent requires a list of RenderedSectionContent for "
                "sections."
            )
        self.sections = sections
        self.data_asset_name = data_asset_name
        self.full_data_asset_identifier = full_data_asset_identifier
        self.renderer_type = renderer_type
        self.page_title = page_title
        self.utm_medium = utm_medium
        self.cta_footer = cta_footer
        self.expectation_suite_name = expectation_suite_name
        self.batch_kwargs = batch_kwargs
        self.batch_spec = batch_spec
        self.ge_cloud_id = ge_cloud_id

    def to_json_dict(self):
        d = super().to_json_dict()
        d["sections"] = RenderedContent.rendered_content_list_to_json(self.sections)
        d["data_asset_name"] = self.data_asset_name
        d["full_data_asset_identifier"] = self.full_data_asset_identifier
        d["renderer_type"] = self.renderer_type
        d["page_title"] = self.page_title
        d["utm_medium"] = self.utm_medium
        d["cta_footer"] = self.cta_footer
        d["expectation_suite_name"] = self.expectation_suite_name
        d["batch_kwargs"] = self.batch_kwargs
        d["batch_spec"] = self.batch_spec
        d["ge_cloud_id"] = self.ge_cloud_id
        return d


class RenderedSectionContent(RenderedContent):
    def __init__(self, content_blocks, section_name=None) -> None:
        if not isinstance(content_blocks, list) and all(
            [
                isinstance(content_block, RenderedComponentContent)
                for content_block in content_blocks
            ]
        ):
            raise InvalidRenderedContentError(
                "Rendered section content requires a list of RenderedComponentContent "
                "for content blocks."
            )
        self.content_blocks = content_blocks
        self.section_name = section_name

    def to_json_dict(self) -> dict:
        d = super().to_json_dict()
        d["content_blocks"] = RenderedContent.rendered_content_list_to_json(
            self.content_blocks
        )
        d["section_name"] = self.section_name
        return d


class RenderedAtomicValue(DictDot):
    def __init__(
        self,
        schema: Optional[dict] = None,
        header: Optional["RenderedAtomicValue"] = None,
        template: Optional[str] = None,
        params: Optional[dict] = None,
        header_row: Optional[List["RenderedAtomicValue"]] = None,
        table: Optional[List[List["RenderedAtomicValue"]]] = None,
        graph: Optional[dict] = None,
        kwargs: Optional[dict] = None,
    ) -> None:
        self.schema: Optional[dict] = schema
        self.header: Optional[RenderedAtomicValue] = header

        # StringValueType
        self.template: Optional[str] = template
        self.params: Optional[dict] = params

        # TableType
        self.header_row: Optional[List[RenderedAtomicValue]] = header_row
        self.table: Optional[List[List[RenderedAtomicValue]]] = table

        # GraphType
        self.graph: Optional[RenderedAtomicValueGraph] = RenderedAtomicValueGraph(
            graph=graph
        )

        # UnknownType
        self.kwargs: Optional[dict] = kwargs

    def __repr__(self) -> str:
        return json.dumps(self.to_json_dict(), indent=2)

    def __str__(self) -> str:
        return json.dumps(self.to_json_dict(), indent=2)

    def to_json_dict(self) -> dict:
        """Returns RenderedAtomicValue as a json dictionary."""
        d = renderedAtomicValueSchema.dump(self)
        json_dict: dict = {}
        for key in d:
            if key == "graph":
                json_dict[key] = getattr(self, key).to_json_dict()
            else:
                json_dict[key] = getattr(self, key)
        return json_dict


class RenderedAtomicValueGraph(DictDot):
    def __init__(
        self,
        graph: Optional[dict] = None,
    ):
        self.graph = graph

    def __repr__(self) -> str:
        return json.dumps(self.to_json_dict(), indent=2)

    def __str__(self) -> str:
        return json.dumps(self.to_json_dict(), indent=2)

    def to_json_dict(self) -> dict:
        """Returns RenderedAtomicValueGraph as a json dictionary."""
        return self.graph


class RenderedAtomicValueSchema(Schema):
    class Meta:
        unknown = INCLUDE

    schema = fields.Dict(required=False, allow_none=True)
    header = fields.Dict(required=False, allow_none=True)

    # for StringValueType
    template = fields.String(required=False, allow_none=True)
    params = fields.Dict(required=False, allow_none=True)

    # for TableType
    header_row = fields.List(fields.Dict, required=False, allow_none=True)
    table = fields.List(fields.List(fields.Dict, required=False, allow_none=True))

    # for GraphType
    graph = fields.Dict(required=False, allow_none=True)

    # for UnknownType
    kwargs = fields.Dict(required=False, allow_none=True)

    @post_load
    def create_value_obj(self, data, **kwargs):
        return RenderedAtomicValue(**data)

    REMOVE_KEYS_IF_NONE = [
        "template",
        "table",
        "params",
        "header_row",
        "table",
        "graph",
        "kwargs",
    ]

    @post_dump
    def clean_null_attrs(self, data: dict, **kwargs: dict) -> dict:
        """Removes the attributes in RenderedAtomicValueSchema.REMOVE_KEYS_IF_NONE during serialization if
        their values are None."""
        data = deepcopy(data)
        for key in RenderedAtomicValueSchema.REMOVE_KEYS_IF_NONE:
            if key == "graph" and key in data and data[key]["graph"] is None:
                data.pop(key)
            elif key in data and data[key] is None:
                data.pop(key)
        return data


class RenderedAtomicContent(RenderedContent):
    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[RenderedAtomicValue] = None,
        value_type: Optional[str] = None,
    ) -> None:
        self.name = name
        self.value = value
        self.value_type = value_type

    def __repr__(self) -> str:
        return json.dumps(self.to_json_dict(), indent=2)

    def __str__(self) -> str:
        return json.dumps(self.to_json_dict(), indent=2)

    def to_json_dict(self) -> dict:
        """Returns RenderedAtomicContent as a json dictionary."""
        d = super().to_json_dict()
        d["name"] = self.name
        d["value"] = self.value.to_json_dict()
        d["value_type"] = self.value_type
        return d


class RenderedAtomicContentSchema(Schema):
    class Meta:
        unknown: INCLUDE

    name = fields.String(required=False, allow_none=True)
    value = fields.Nested(RenderedAtomicValueSchema(), required=True, allow_none=False)
    value_type = fields.String(required=True, allow_none=False)

    @post_load
    def make_rendered_atomic_content(self, data, **kwargs):
        return RenderedAtomicContent(**data)


renderedAtomicValueSchema = RenderedAtomicValueSchema()
