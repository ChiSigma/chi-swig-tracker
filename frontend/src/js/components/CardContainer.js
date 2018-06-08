/**
 * Created by alexmelagrano on 5/11/18.
 */
import React from 'react';

import MiniProfileCard from './MiniProfileCard';
import ProfileCard from './ProfileCard';
import ProgressBar from './ProgressBar';

export default class CardContainer extends React.Component {
    constructor(props) {
        super(props);

        this.appState = () => { return this.props.context.state };
        this.cache = () => { return this.props.context.cache };

        this.state = {
            show: false,
            sortOrder: [],
            eventTypes: {},
            eventTimes: [],
            profiles: {},
            loading: true
        };
        
        this.activeProfile = {};

        this.handleShow = this.handleShow.bind(this);
        this.handleClose = this.handleClose.bind(this);
    }

    async fetchSort(sortEventType=this.appState().sortEventType, sortTime=this.appState().sortTime) {
        const filterQuery = this.appState().filterQuery();
        const profileType = this.appState().profileType;
        return await fetch('api/' + profileType + '/sort?time=' + sortTime + '&event_type_id=' + sortEventType + '&' + filterQuery, {credentials: "same-origin"});
    }

    async updateSort(newSortEventType=false, newSortTime=false) {
        const sortEventType = newSortEventType ? newSortEventType : this.appState().sortEventType;
        const sortTime = newSortTime ? newSortTime : this.appState().sortTime;
        const sortOrder = await this.fetchSort(sortEventType, sortTime);
        const profiles = await this.cache().fetchAll(sortOrder)

        let newState = {profiles: profiles, sortOrder: sortOrder, loading: false};
        this.setState(newState);
    }

    componentDidUpdate(prevProps, prevState) {
        const cacheDoneHydrating = !prevProps.context.state.isHydrated && this.appState().isHydrated;
        const toggledViews = prevProps.context.state.view !== 'dashboard';
        if (cacheDoneHydrating || toggledViews) {
            return this.hydrateCardContainer();
        }
        const contextSortEventType = this.appState().sortEventType;
        const contextSortTime = this.appState().sortTime;
        const appStateChanged = this.appState().hasChanged(prevProps);
        if (appStateChanged && !this.state.loading) {
            this.setState({loading: true});
            this.updateSort(contextSortEventType, contextSortTime);
        }
    }

    componentWillMount() {
        if (this.appState().lastView() !== 'dashboard') {
            return this.hydrateCardContainer();
        }
    }

    async hydrateCardContainer() {
        let sort = this.fetchSort();
        let version = this.appState().refreshVersion();
        sort = await sort;
        await version;
        const profiles = await this.cache().fetchAll(sort);
        this.setState({
                profiles: profiles,
                sortOrder: sort,
                loading: false
            });
        this.interval = setInterval(this.autoRefresh.bind(this), 30000)
    }

    async componentDidMount() {
        const eventInfo = await fetch('api/event_types');

        this.setState({
            showStats: 0,
            flipClass: "",
            eventTypes: eventInfo['event_types'],
            eventTimes: eventInfo['times']
        });
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    async handleRefresh() {
        await this.appState().refreshVersion();
    }

    autoRefresh() {
        if (this.appState().autoRefresh) {
            this.handleRefresh();
        }
    }

    async handleClose() {
        this.setState({ show: false, showStats: 0, flipClass: "" })
        await this.handleRefresh();
    }

    handleShow() {
        console.log('showing the modal');
        this.setState({ show: true })
    }

    changeActiveProfile(activeProfile) {
        this.activeProfile = activeProfile;
        this.handleShow();
    }

    toggleStats(e) {
        /* 0 = Use regular hover, 1 means show stats, 2 means show front (hover disabled) */
        e.stopPropagation();
        const currentState = this.state.showStats;
        const newState = (currentState + 1) % 3
        
        let newFlipClass = "";
        if (newState === 1) {
            newFlipClass = "hover";
        } else if (newState === 2) {
            newFlipClass = "disable-hover";
        }

        this.setState({showStats: newState, flipClass: newFlipClass});
    }
    
    render() {

        const miniProfiles = this.state.sortOrder.map((profileId) =>
            <div className="m-4">
                <MiniProfileCard changeActiveProfile={ this.changeActiveProfile.bind(this) } activeProfile={ this.state.profiles[profileId] } />
            </div>
        );

        const modal = this.state.show ? (
            <div className="d-block modal">
                <div className="bg-gray-transparent modal-backdrop h-100 d-flex justify-content-center align-items-center" onClick={ this.handleClose }>
                    <div className={ "flip-container " + this.state.flipClass } onClick={ this.toggleStats.bind(this) }>
                        <ProfileCard profile={ this.activeProfile } context={ this.props.context } eventTypes={ this.state.eventTypes } eventTimes={ this.state.eventTimes } />
                    </div>
                </div>
            </div>
        ) : (
            console.log('hiding the modal!')
        );

        const loadingOverlay = this.state.loading ? (
                <div id="card-container-loading">
                    <ProgressBar />
                </div>
            ) : (
                console.log('finished loading!')
            );

        return (
            <div className="container pt-4">
                { modal }
                <div className="row">
                    { loadingOverlay }
                    <div className="d-flex align-items-baseline justify-content-center flex-wrap">
                            { miniProfiles }
                    </div>
                </div>
            </div>
        )
    }
}
