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
                myPrivacySetting: async function () {
                    const user = await this.state.auth.me()
                    return user.privacy_setting;
                }.bind(this),
                me: async function() {
                    return await this.state.auth.currentUser ? Promise.resolve(this.state.auth.currentUser) : this.fetchMe();
                }.bind(this),
            },
            state: {
                sortEventType: 1,
                sortTime: '*',
                autoRefresh: false,
                profileType: 'drinkers',
                groups: [],
                drinkers: [],
                updateSort: function(sortEventType=1, sortTime='*') {
                    console.log({ sortEventType, sortTime })
                    let state = { ...this.state.state }
                    state.sortEventType = sortEventType;
                    state.sortTime = sortTime;
                    this.setState({ state });
                }.bind(this),
                toggleAutoRefresh: function() {
                    let state = { ...this.state.state }
                    state.autoRefresh = !this.state.state.autoRefresh;
                    this.setState({ state });
                }.bind(this),
                filterQuery: function() {
                    return this.sortFilters();
                }.bind(this),
                eventsQuery: function(id) {
                    return this.createEventFilter(id);
                }.bind(this)
            },
            cache: {
                drinkers: {},
                groups: {},
                fetch: async function(id) {
                    const type = this.state.state.profileType;
                    let obj = await this.state.cache[type][id] ? Promise.resolve(this.state.cache[type][id]) : this.fetchObjs(type, [id])[0];
                    if (!this.state.cache[type][id]) this.state.cache[type][id] = obj;
                    return obj;
                }.bind(this),
                fetchAll: async function(ids) {
                    const type = this.state.state.profileType;
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
        const me = this.state.auth.me();
        const initalGroup = me.primary_group_id ? me.primary_group_id : 2;
        let state = { ...this.state.state };
        state.groups = [initalGroup];
        this.setState( { state } );
    }

    sortFilters() {
        let filters = [];
        let groupIds = this.state.state.groups.join(',');
        let drinkerIds = this.state.state.drinkers.join(',');
        if (drinkerIds) filters.push('drinker_ids=' + drinkerIds);
        if (groupIds) filters.push('group_ids=' + groupIds);
        return filters.join('&');
    }

    createEventFilter(id) {
        let filter = this.state.state.profileType === 'groups' ? 'group_ids=' : 'drinker_ids=';
        return filter += id;
    }

    async fetchObjs(type, ids) {
        const objResp = await fetch('api/' + type + '/?ids=' + ids.join(','), {credentials: 'same-origin'})
        const objs = await objResp.json()
        return objs[type]
    }

    async fetchMe() {
        const userResp = await fetch('auth/me', {credentials: 'same-origin'})
        const user = await userResp.json();
        let auth = { ...this.state.auth }
        auth.currentUser = user;
        this.setState({ auth });
        return user;
    }

    render() {
        return (
            <AppContext.Provider value={ this.state }>
                {this.props.children}
            </AppContext.Provider>
        );
    }
}