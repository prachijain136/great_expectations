import json

import jsonschema
import pytest

from great_expectations.core.usage_statistics.events import UsageStatsEvents
from great_expectations.core.usage_statistics.schemas import (
    anonymized_batch_request_schema,
    anonymized_batch_schema,
    anonymized_checkpoint_run_schema,
    anonymized_cli_new_ds_choice_payload_schema,
    anonymized_cli_suite_expectation_suite_payload_schema,
    anonymized_datasource_schema,
    anonymized_datasource_sqlalchemy_connect_payload_schema,
    anonymized_get_or_edit_or_save_expectation_suite_payload_schema,
    anonymized_init_payload_schema,
    anonymized_legacy_profiler_build_suite_payload_schema,
    anonymized_rule_based_profiler_run_schema,
    anonymized_run_validation_operator_payload_schema,
    anonymized_test_yaml_config_payload_schema,
    anonymized_usage_statistics_record_schema,
    empty_payload_schema,
)
from great_expectations.data_context.util import file_relative_path
from tests.integration.usage_statistics.test_usage_statistics_messages import (
    valid_usage_statistics_messages,
)


def test_comprehensive_list_of_messages():
    """Ensure that we have a comprehensive set of tests for known messages, by
    forcing a manual update to this list when a message is added or removed, and
    reminding the developer to add or remove the associate test."""
    valid_message_list = list(valid_usage_statistics_messages.keys())
    # NOTE: If you are changing the expected valid message list below, you need
    # to also update one or more tests below!

    assert set(valid_message_list) == {
        "cli.checkpoint.delete",
        "cli.checkpoint.list",
        "cli.checkpoint.new",
        "cli.checkpoint.run",
        "cli.checkpoint.script",
        "cli.datasource.delete",
        "cli.datasource.list",
        "cli.datasource.new",
        "cli.datasource.profile",
        "cli.docs.build",
        "cli.docs.clean",
        "cli.docs.list",
        "cli.init.create",
        "cli.new_ds_choice",
        "cli.project.check_config",
        "cli.project.upgrade",
        "cli.store.list",
        "cli.suite.delete",
        "cli.suite.demo",
        "cli.suite.edit",
        "cli.suite.list",
        "cli.suite.new",
        "cli.suite.scaffold",
        "cli.validation_operator.list",
        "cli.validation_operator.run",
        "data_asset.validate",
        "data_context.__init__",
        "data_context.add_datasource",
        "data_context.get_batch_list",
        "data_context.build_data_docs",
        "data_context.open_data_docs",
        "data_context.run_checkpoint",
        "data_context.save_expectation_suite",
        "data_context.test_yaml_config",
        "data_context.run_validation_operator",
        "datasource.sqlalchemy.connect",
        "execution_engine.sqlalchemy.connect",
        "checkpoint.run",
        "expectation_suite.add_expectation",
        "legacy_profiler.build_suite",
        "profiler.run",
        "data_context.run_profiler_on_data",
        "data_context.run_profiler_with_dynamic_arguments",
        "profiler.result.get_expectation_suite",
        "data_assistant.result.get_expectation_suite",
    }
    # Note: "cli.project.upgrade" has no base event, only .begin and .end events
    assert set(valid_message_list) == set(
        UsageStatsEvents.get_all_event_names_no_begin_end_events()
        + ["cli.project.upgrade"]
    )


def test_init_message():
    usage_stats_records_messages = [
        "data_context.__init__",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            # non-empty payload
            jsonschema.validate(
                message["event_payload"],
                anonymized_init_payload_schema,
            )


def test_data_asset_validate_message():
    usage_stats_records_messages = [
        "data_asset.validate",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            # non-empty payload
            jsonschema.validate(
                message["event_payload"],
                anonymized_batch_schema,
            )


def test_data_context_add_datasource_message():
    usage_stats_records_messages = [
        "data_context.add_datasource",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            # non-empty payload
            jsonschema.validate(
                message["event_payload"],
                anonymized_datasource_schema,
            )


def test_data_context_get_batch_list_message():
    usage_stats_records_messages = [
        "data_context.get_batch_list",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            jsonschema.validate(
                message["event_payload"],
                anonymized_batch_request_schema,
            )


def test_checkpoint_run_message():
    usage_stats_records_messages = [
        "checkpoint.run",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            jsonschema.validate(
                message["event_payload"],
                anonymized_checkpoint_run_schema,
            )


def test_run_validation_operator_message():
    usage_stats_records_messages = ["data_context.run_validation_operator"]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            jsonschema.validate(
                message["event_payload"],
                anonymized_run_validation_operator_payload_schema,
            )


def test_legacy_profiler_build_suite_message():
    usage_stats_records_messages = [
        "legacy_profiler.build_suite",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            jsonschema.validate(
                message["event_payload"],
                anonymized_legacy_profiler_build_suite_payload_schema,
            )


def test_data_context_save_expectation_suite_message():
    usage_stats_records_messages = [
        "data_context.save_expectation_suite",
        "profiler.result.get_expectation_suite",
        "data_assistant.result.get_expectation_suite",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            jsonschema.validate(
                message["event_payload"],
                anonymized_get_or_edit_or_save_expectation_suite_payload_schema,
            )


def test_datasource_sqlalchemy_connect_message():
    usage_stats_records_messages = [
        "datasource.sqlalchemy.connect",
        "execution_engine.sqlalchemy.connect",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            jsonschema.validate(
                message["event_payload"],
                anonymized_datasource_sqlalchemy_connect_payload_schema,
            )


def test_cli_data_asset_validate():
    usage_stats_records_messages = [
        "data_asset.validate",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:

            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )


def test_cli_new_ds_choice_message():
    usage_stats_records_messages = [
        "cli.new_ds_choice",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # non-empty payload
            jsonschema.validate(
                message["event_payload"],
                anonymized_cli_new_ds_choice_payload_schema,
            )


def test_cli_suite_new_message():
    usage_stats_records_messages = [
        "cli.suite.new",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            jsonschema.validate(
                message["event_payload"],
                anonymized_cli_suite_expectation_suite_payload_schema,
            )


def test_cli_suite_edit_message():
    usage_stats_records_messages = [
        "cli.suite.edit",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            jsonschema.validate(
                message["event_payload"],
                anonymized_cli_suite_expectation_suite_payload_schema,
            )


@pytest.mark.slow  # 2.42s
def test_test_yaml_config_messages():
    usage_stats_records_messages = [
        "data_context.test_yaml_config",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            # record itself
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            jsonschema.validate(
                message["event_payload"],
                anonymized_test_yaml_config_payload_schema,
            )


def test_usage_stats_empty_payload_messages():
    usage_stats_records_messages = [
        "data_context.build_data_docs",
        "data_context.open_data_docs",
        "data_context.run_checkpoint",
        "data_context.run_profiler_on_data",
        "data_context.run_profiler_with_dynamic_arguments",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            jsonschema.validate(
                message["event_payload"],
                empty_payload_schema,
            )


def test_usage_stats_expectation_suite_messages():
    usage_stats_records_messages = [
        "expectation_suite.add_expectation",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            jsonschema.validate(
                message["event_payload"],
                empty_payload_schema,
            )


@pytest.mark.slow  # 5.20s
def test_usage_stats_cli_payload_messages():
    usage_stats_records_messages = [
        "cli.checkpoint.delete",
        "cli.checkpoint.list",
        "cli.checkpoint.new",
        "cli.checkpoint.run",
        "cli.checkpoint.script",
        "cli.datasource.delete",
        "cli.datasource.list",
        "cli.datasource.new",
        "cli.datasource.profile",
        "cli.docs.build",
        "cli.docs.clean",
        "cli.docs.list",
        "cli.init.create",
        "cli.project.check_config",
        "cli.project.upgrade",
        "cli.store.list",
        "cli.suite.delete",
        "cli.suite.demo",
        "cli.suite.list",
        "cli.suite.new",
        "cli.suite.scaffold",
        "cli.validation_operator.list",
        "cli.validation_operator.run",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )


def test_rule_based_profiler_run_message():
    usage_stats_records_messages = [
        "profiler.run",
    ]
    for message_type in usage_stats_records_messages:
        for message in valid_usage_statistics_messages[message_type]:
            jsonschema.validate(
                message,
                anonymized_usage_statistics_record_schema,
            )
            jsonschema.validate(
                message["event_payload"],
                anonymized_rule_based_profiler_run_schema,
            )


def test_usage_stats_schema_in_codebase_is_up_to_date() -> None:
    path: str = file_relative_path(
        __file__,
        "../../../great_expectations/core/usage_statistics/usage_statistics_record_schema.json",
    )
    with open(path) as f:
        contents: dict = json.load(f)

    assert contents == anonymized_usage_statistics_record_schema
