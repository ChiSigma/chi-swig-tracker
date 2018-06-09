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
import DrinkerForm from './DrinkerForm';
import DrinkerMembershipTable from './DrinkerMembershipTable';

const styles = theme => ({
    root: {
        width: '100%',
    },
    heading: {
        fontSize: theme.typography.pxToRem(15),
        fontWeight: theme.typography.fontWeightRegular,
    },
});

function DrinkerTable(props) {
    const { classes } = props;
    const drinkers = props.drinkers;
    const admin = props.admin;

    const drinkerPanels = drinkers.map((drinker) =>
        <ExpansionPanel key={ drinker.id }>
            <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                <DrinkerForm drinker={ drinker } onSubmit={ async (drinker) => {return await admin.edit('drinkers', drinker);} }/>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails>
                <DrinkerMembershipTable drinker={ drinker }
                                        groupSuggestions={ props.groupSuggestions }
                                        onSubmit={ async (membership) => {return await admin.editMembership('drinkers', drinker, membership);} }
                                        onDelete={ async (membership) => {return await admin.deleteMembership('drinkers', drinker, membership);} } 
                                        fetchMemberships={ async () => {return await admin.fetchMemberships('drinkers', drinker);} } />
            </ExpansionPanelDetails>
        </ExpansionPanel>
    );
    
    return (
        <div className={classes.root}>
            { drinkerPanels }
        </div>
    );
}

DrinkerTable.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(DrinkerTable);