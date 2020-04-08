------------------------------------------------------------------------------
-- Clear and load SymmetricDS Configuration
------------------------------------------------------------------------------

delete from sym_trigger_router;
delete from sym_trigger;
delete from sym_router;
delete from sym_channel where channel_id in ('main_channel');
delete from sym_node_group_link;
delete from sym_node_group;
delete from sym_node_host;
delete from sym_node_identity;
delete from sym_node_security;
delete from sym_node;

------------------------------------------------------------------------------
-- Channels
------------------------------------------------------------------------------

-- Channel "sensor_data" for tables related to items for purchase
insert into sym_channel
(channel_id, processing_order, max_batch_size, enabled, description)
values('main_channel', 1, 100000, 1, 'Main channel for mercury');

------------------------------------------------------------------------------
-- Node Groups
------------------------------------------------------------------------------

insert into sym_node_group (node_group_id) values ('group0');
insert into sym_node_group (node_group_id) values ('group1');

------------------------------------------------------------------------------
-- Node Group Links
------------------------------------------------------------------------------

-- Corp sends changes to Store when Store pulls from Corp
insert into sym_node_group_link (source_node_group_id, target_node_group_id, data_event_action) values ('group0', 'group1', 'P');

-- Store sends changes to Corp when Store pushes to Corp
insert into sym_node_group_link (source_node_group_id, target_node_group_id, data_event_action) values ('group1', 'group0', 'P');

------------------------------------------------------------------------------
-- Triggers
------------------------------------------------------------------------------

insert into sym_trigger
(trigger_id,source_table_name,channel_id,last_update_time,create_time)
values('all_mercury_table_trigger','ag_*','main_channel',current_timestamp,current_timestamp);

------------------------------------------------------------------------------
-- Routers
------------------------------------------------------------------------------

-- Default router sends all data from corp to store
insert into sym_router
(router_id,source_node_group_id,target_node_group_id,router_type,create_time,last_update_time)
values('group0_to_1', 'group0', 'group1', 'default',current_timestamp, current_timestamp);

-- Default router sends all data from store to corp
insert into sym_router
(router_id,source_node_group_id,target_node_group_id,router_type,create_time,last_update_time)
values('group1_to_0', 'group1', 'group0', 'default',current_timestamp, current_timestamp);

------------------------------------------------------------------------------
-- Trigger Routers
------------------------------------------------------------------------------

insert into sym_trigger_router
(trigger_id,router_id,initial_load_order,last_update_time,create_time)
values('all_mercury_table_trigger','group0_to_1', 100, current_timestamp, current_timestamp);

insert into sym_trigger_router
(trigger_id,router_id,initial_load_order,last_update_time,create_time)
values('all_mercury_table_trigger','group1_to_0', 100, current_timestamp, current_timestamp);
