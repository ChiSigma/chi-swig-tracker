/**
 * Created by alexmelagrano on 5/11/18.
 */
import React from 'react';

import MiniProfileCard from './MiniProfileCard';
import ProfileCard from './ProfileCard';

export default class CardContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            show: false,
            sortEventType: props.context.sortEventType,
            sortTime: props.context.sortTime,
            sortOrder: [],
            drinkers: {},
            eventTypes: {},
            eventTimes: [],
            version: ''
        };
        
        this.activeProfile = {};

        this.handleShow = this.handleShow.bind(this);
        this.handleClose = this.handleClose.bind(this);
    }

    async fetchSort(sortEventType=this.state.sortEventType, sortTime=this.state.sortTime) {
        const sortRes = await fetch('api/drinkers/sort?time=' + sortTime + '&event_type_id=' + sortEventType);
        return await sortRes.json();
    }

    async updateSort(newVersion=false, newSortEventType=false, newSortTime=false) {
        const sortEventType = newSortEventType ? newSortEventType : this.state.sortEventType;
        const sortTime = newSortTime ? newSortTime : this.state.sortTime;
        const sortOrder = await this.fetchSort(sortEventType, sortTime);

        let newState = {sortOrder: sortOrder};
        if (newVersion) newState['version'] = newVersion;
        if (newSortEventType) newState['sortEventType'] = newSortEventType;
        if (newSortTime) newState['sortTime'] = newSortTime;

        this.setState(newState);
    }

    async fetchDrinkers() {
        const drinkersRes = await fetch('api/drinkers/');
        return await drinkersRes.json();
    }

    async fetchVersion() {
        const versionRes = await fetch('api/drinkers/version');
        return versionRes.json();
    }

    componentDidUpdate(prevProps, prevState) {
        const contextSortEventType = this.props.context.sortEventType;
        const contextSortTime = this.props.context.sortTime;
        if (contextSortEventType !== this.state.sortEventType || contextSortTime !== this.state.sortTime) {
            this.updateSort(false, contextSortEventType, contextSortTime);
        }
    }

    async componentWillMount() {
        const drinkersData = await this.fetchDrinkers();
        const sort = await this.fetchSort()
        let version = drinkersData['version'];
        let drinkers = drinkersData['drinkers']
        let drinkersHash = {}
        for (var drinker of drinkers) {
            drinkersHash[drinker['id']] = drinker
        }

        this.setState({
                drinkers: drinkersHash,
                version: version,
                sortOrder: sort,
                activeProfile: drinkersHash[sort[0]],
                showStats: 0,
                flipClass: ""
            });
    }

    async componentDidMount() {
        const eventTypesResp = await fetch('api/event_types/');
        const eventInfo = await eventTypesResp.json();

        this.setState({eventTypes: eventInfo['event_types'], eventTimes: eventInfo['times']})
    }

    handleClose() {
        this.setState({ show: false, showStats: 0, flipClass: "" })
        this.fetchVersion().then(function(version) {
            if(version !== this.state.version) {
                this.updateSort(version);
            }
        }.bind(this))
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
                <MiniProfileCard changeActiveProfile={ this.changeActiveProfile.bind(this) } activeProfile={ this.state.drinkers[profileId] } />
            </div>
        );
        const modal = this.state.show ? (
            <div className="d-block modal">
                <div className="bg-gray-transparent modal-backdrop h-100 d-flex justify-content-center align-items-center" onClick={ this.handleClose }>
                    <div className={ "flip-container " + this.state.flipClass } onClick={ this.toggleStats.bind(this) }>
                        <ProfileCard profile={ this.activeProfile } eventTypes={ this.state.eventTypes } eventTimes={ this.state.eventTimes } />
                    </div>
                </div>
            </div>
        ) : (
            console.log('hiding the modal!')
        );

        return (
            <div className="container pt-4">
                { modal }
                <div className="row">
                    <div className="d-flex align-items-baseline justify-content-center flex-wrap">
                            { miniProfiles }
                    </div>
                </div>
            </div>
        )
    }
}
