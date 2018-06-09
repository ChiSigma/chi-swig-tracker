import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import GroupForm from './GroupForm';
import GroupMembershipTable from './GroupMembershipTable';

const styles = theme => ({
    root: {
        width: '100%',
    },
    heading: {
        fontSize: theme.typography.pxToRem(15),
        fontWeight: theme.typography.fontWeightRegular,
    },
});

function GroupTable(props) {
    const { classes } = props;
    const groups = props.groups;
    const admin = props.admin;

    const groupPanels = groups.map((group) =>
        <ExpansionPanel key={ group.id }>
            <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                <GroupForm group={ group } onSubmit={ async (group) => {return await admin.edit('groups', group);} }/>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails>
                <GroupMembershipTable   group={ group }
                                        drinkerSuggestions={ props.drinkerSuggestions }
                                        onSubmit={ async (membership) => {return await admin.editMembership('groups', group, membership);} }
                                        onDelete={ async (membership) => {return await admin.deleteMembership('groups', group, membership);} } 
                                        fetchMemberships={ async () => {return await admin.fetchMemberships('groups', group);} } />
            </ExpansionPanelDetails>
        </ExpansionPanel>
    );
    
    return (
        <div className={classes.root}>
            { groupPanels }
        </div>
    );
}

GroupTable.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(GroupTable);