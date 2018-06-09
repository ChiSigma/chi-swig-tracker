import React from 'react';

import ProgressBar from '../ProgressBar';
import DrinkerTable from './DrinkerTable';
import GroupTable from './GroupTable';

export default class AdminContainer extends React.Component {
    constructor(props) {
        super(props);
        this.admin = () => { return this.props.context.admin; }
        this.state = {
            drinkers: [],
            groups: [],
            drinkerSuggestions: {},
            groupSuggestions: {},
            loading: true
        }
    }

    async componentDidMount() {
        let drinkers = this.admin().fetch('drinkers');
        let groups = this.admin().fetch('groups');
        let groupSuggestions = this.admin().fetchSuggestions('groups');
        let drinkerSuggestions = this.admin().fetchSuggestions('drinkers');
        drinkers = await drinkers;
        groups = await groups;
        groupSuggestions = await groupSuggestions;
        drinkerSuggestions = await drinkerSuggestions;

        this.setState({ drinkers, groups, drinkerSuggestions, groupSuggestions, loading: false })
    }

    render() {
        const loadingOverlay = () => {
                if (this.state.loading) return (
                    <div id="card-container-loading">
                        <ProgressBar />
                    </div>
                );
        }

        return (
            <div>
                { loadingOverlay() }`
                <div id="adminContainer" className="container col-lg-8">
                    <div id="editDrinkers">
                        <h3>Edit Drinkers</h3>
                        <DrinkerTable drinkers={ this.state.drinkers.sort((first,second) => {return first.name.localeCompare(second.name)}) } groupSuggestions={ this.state.groupSuggestions } admin={ this.admin() } />
                    </div>
                    <div id="editGroups">
                        <h3>Edit Groups</h3>
                        <GroupTable groups={ this.state.groups.sort((first,second) => {return first.name.localeCompare(second.name)}) } drinkerSuggestions={ this.state.drinkerSuggestions } admin={ this.admin() } />
                    </div>
                </div>
            </div>
        )
    }
}