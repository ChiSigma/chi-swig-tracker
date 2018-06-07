import React, {Component} from 'react';
import AppContext from '../app-context';

export default class AppProvider extends Component {
    constructor() {
        super();
        this.state = {
            auth: {
                currentUser: false,
                isLoggedIn: async function() {
                    const user = await this.state.auth.me()
                    return !!user.id;
                }.bind(this),
                isEditable: async function(profile) {
                    const user = await this.state.auth.me();
                    const userGroups = user.groups_can_edit || []
                    const profileGroups = profile.groups_can_edit || []
                    return profileGroups.some((e) => {
                        return userGroups.includes(e);
                    });
                }.bind(this),
                myPrivacySetting: async function () {
                    const user = await this.state.auth.me();
                    return user.privacy_setting;
                }.bind(this),
                me: async function() {
                    const user = await this.state.auth.currentUser ? Promise.resolve(this.state.auth.currentUser) : this.fetchMe();
                    let auth = { ...this.state.auth }
                    auth.currentUser = user;
                    this.setState({ auth });
                    return user;
                }.bind(this),
            },
            state: {
                sortEventType: 1,
                sortTime: '*',
                autoRefresh: false,
                profileType: 'drinkers',
                groups: [],
                drinkers: [],
                version: {},
                isHydrated: false,
                checkVersion: async function({ groups, drinkers, profileType}) {
                    const version = await this.fetchVersion({ groups, drinkers, profileType});
                    return version;
                }.bind(this),
                refreshVersion: async function() {
                    let state = { ...this.state.state };
                    const version = await this.fetchVersion();
                    state.version = version;
                    this.setState({ state });
                }.bind(this),
                updateSort: function(sortEventType=1, sortTime='*') {
                    let state = { ...this.state.state };
                    state.sortEventType = sortEventType;
                    state.sortTime = sortTime;
                    this.setState({ state });
                }.bind(this),
                updateFilters: async function({ drinkers, groups, profileType }) {
                    let state = { ...this.state.state };
                    state.drinkers = drinkers;
                    state.groups = groups;
                    state.profileType = profileType;

                    const version = await this.fetchVersion({ groups, drinkers, profileType });
                    state.version = version;
                    this.setState({ state });
                }.bind(this),
                toggleAutoRefresh: function() {
                    let state = { ...this.state.state }
                    state.autoRefresh = !this.state.state.autoRefresh;
                    this.setState({ state });
                }.bind(this),
                filterQuery: function({ groups = false, drinkers = false } = {}) {
                    return this.sortFilters({ groups, drinkers });
                }.bind(this),
                eventsQuery: function(id) {
                    return this.createEventFilter(id);
                }.bind(this),
                hasChanged: function(prevProps) {
                    const prevAppState = prevProps.context.state;
                    const curAppState = this.state.state;
                    if (curAppState.sortTime !== prevAppState.sortTime) return true;
                    if (curAppState.sortEventType !== prevAppState.sortEventType) return true;
                    if (curAppState.profileType !== prevAppState.profileType) return true;
                    if (curAppState.version.version !== prevAppState.version.version) return true;
                    if (curAppState.drinkers.sort().toString() !== prevAppState.drinkers.sort().toString()) return true;
                    if (curAppState.groups.sort().toString() !== prevAppState.groups.sort().toString()) return true;

                    return false;
                }.bind(this)
            },
            cache: {
                drinkers: {},
                groups: {},
                fetchFilterSuggestions: async function(type, groups, drinkers) {
                    let filter = type === 'groups' ? this.sortFilters({ groups: [], drinkers }) : this.sortFilters({ groups, drinkers: [] });
                    let objs = await this.fetchObjs(type, [], filter);
                    objs.forEach((obj) => {
                        this.state.cache[type][obj.id] = obj
                    });

                    return objs;
                }.bind(this),
                fetch: async function(id, type=this.state.state.profileType) {
                    let obj = await this.state.cache[type][id] ? Promise.resolve(this.state.cache[type][id]) : this.fetchObjs(type, [id])[0];
                    if (!this.state.cache[type][id]) this.state.cache[type][id] = obj;
                    return obj;
                }.bind(this),
                fetchAll: async function(ids, type=this.state.state.profileType) {
                    let hits = {};
                    let misses = [];
                    ids.forEach((id) => {
                       if (this.state.cache[type][id]) {
                        hits[id] = this.state.cache[type][id]
                       } else {
                        misses.push(id);
                       }
                    });
                    let objs = misses.length > 0 ? await this.fetchObjs(type, misses) : [];
                    objs.forEach((obj) => {
                        hits[obj.id] = obj;
                        this.state.cache[type][obj.id] = obj
                    });

                    return hits;
                }.bind(this),
                poke: async function(ids) {
                    this.state.cache.fetchAll(ids);
                }.bind(this)
            }
        }
    }

    async componentWillMount() {
        const me = await this.fetchMe();
        const initialGroup = me.primary_group ? me.primary_group.id : 2;
        let state = { ...this.state.state };
        state.groups = [initialGroup];
        state.isHydrated = true;

        let auth = { ...this.state.auth };
        auth.currentUser = me
        this.setState( { state, auth } );
    }

    sortFilters({ groups = false, drinkers = false } = {}) {
        let filters = [];
        let groupIds = groups ? groups : this.state.state.groups.join(',');
        let drinkerIds = drinkers ? drinkers : this.state.state.drinkers.join(',');
        if (drinkerIds && drinkerIds.length > 0) filters.push('drinker_ids=' + drinkerIds);
        if (groupIds && groupIds.length > 0) filters.push('group_ids=' + groupIds);
        return filters.join('&');
    }

    createEventFilter(id) {
        let filter = this.state.state.profileType === 'groups' ? 'group_ids=' : 'drinker_ids=';
        return filter += id;
    }

    async fetchObjs(type, ids, filters=false) {
        let query = 'api/' + type + '/?ids=' + ids.join(',')
        if (filters) query += ('&' + filters);
        const objs = await fetch(query, {credentials: 'same-origin'})
        
        return objs[type]
    }

    async fetchMe() {
        return await fetch('auth/me', {credentials: 'same-origin'});
    }

    async fetchVersion({ groups = false, drinkers = false, profileType = false } = {}) {
        let state = { ...this.state.state }
        const filterQuery = state.filterQuery({ groups, drinkers });
        profileType = profileType ? profileType : state.profileType;

        return await fetch('api/' + profileType + '/version?' + filterQuery, {credentials: "same-origin"});
    }

    render() {
        return (
            <AppContext.Provider value={ this.state }>
                {this.props.children}
            </AppContext.Provider>
        );
    }
}