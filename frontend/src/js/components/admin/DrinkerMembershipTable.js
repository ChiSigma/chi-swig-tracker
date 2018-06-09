import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import DrinkerMembershipForm from './DrinkerMembershipForm';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
  menu: {
    width: 200,
  },
});

class DrinkerMembershipTable extends React.Component {
  state = { 
            drinker: this.props.drinker, 
            groupSuggestions: this.props.groupSuggestions,
            onSubmit: this.props.onSubmit,
            onDelete: this.props.onDelete,
            memberships: {}
          };

  async componentDidMount() {
    const hashMemberships = await this.fetchMemberships();
    this.setState({ memberships: hashMemberships })
  }

  async fetchMemberships() {
    const memberships = await this.props.fetchMemberships();
    const hashMemberships = {}
    memberships.forEach((membership) => {
                        hashMemberships[membership.id] = membership;
                    })
    return hashMemberships;
  }

  async onSubmit(membership) {
    const resp = await this.state.onSubmit(membership);

    if (resp) {
      const memberships = this.state.memberships;
      if (membership.id === 'unsaved') delete memberships['unsaved'];
      memberships[resp.id] = resp;
      this.setState({ memberships })
    }

    return resp;
  }

  async onDelete(membership) {
    const resp = await this.state.onDelete(membership);

    if (resp) {
      const memberships = this.state.memberships;
      delete memberships[membership.id]
      this.setState({ memberships })
    }

    return resp;
  }

  newMembership() {
    const memberships = this.state.memberships;
    if (memberships['unsaved']) return;
    memberships['unsaved'] = {id: 'unsaved', admin: false, drinker_id: this.props.drinker.id, type: 'primary', changed: true}
    this.setState({ memberships })
  }

  render() {
    const memberships = Object.keys(this.state.memberships).map((id) => this.state.memberships[id]).sort();
    const membershipRows = memberships.map((membership) =>
        <DrinkerMembershipForm  membership={ membership }
                                drinker={ this.state.drinker }
                                groupSuggestions={ this.state.groupSuggestions }
                                onSubmit={ this.onSubmit.bind(this) }
                                onDelete={ this.onDelete.bind(this) } />
    );
    const newMembershipButton = () => {
      if (!this.state.memberships['unsaved']) return (<button onClick={ (e) => { e.stopPropagation(); this.newMembership(); } } className="btn btn-info btn-md">New Membership</button>);
    }
    
    return (
        <div>
            <h6>Memberships</h6>
            { membershipRows }
            { newMembershipButton() }
        </div>
    );  
  }
}

DrinkerMembershipTable.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(DrinkerMembershipTable);
