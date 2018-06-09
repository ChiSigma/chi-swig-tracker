import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';

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

const privacySettings = [
  {
    value: 'public',
    label: 'Public'
  },
  {
    value: 'hide_events',
    label: 'Hide Events',
  },
  {
    value: 'unlisted',
    label: 'Unlisted',
  },
];

const membershipPolicies = [
  {
    value: 'open',
    label: 'Open',
  },
  {
    value: 'primary',
    label: 'Primary Only',
  },
  {
    value: 'ephemeral',
    label: 'Ephemeral Only',
  },
  {
    value: 'private',
    label: 'Private',
  },

]

class GroupForm extends React.Component {
  state = { ...this.props.group, changed: false };

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value,
      changed: true
    });
  };

  async handleSubmit(e) {
    e.preventDefault();
    const resp = await this.props.onSubmit(this.state);
    if (resp && resp.id) {
      this.setState({ ...resp, changed: false });
    }
  }

  render() {
    const { classes } = this.props;
    const saveButton = function() {
      if (this.state.changed) {
        return (
          <button onClick={ (e) => { e.stopPropagation() } } className="btn btn-primary btn-sm" type="submit">save</button>
        )
      }
    }.bind(this)

    return (
      <form className={classes.container} 
            onKeyPress={(e) => { if (e.key === 'Enter') e.preventDefault(); return; }} 
            onSubmit={(e) => { this.handleSubmit(e); }} 
            autoComplete="off">
        <TextField
          required
          id="name"
          label="Name"
          className={classes.textField}
          value={this.state.name}
          onChange={this.handleChange('name')}
          onClick={ (e) => { e.stopPropagation() } }
          margin="normal"
        />
        <TextField
          id="profilePhoto"
          label="Profile Photo"
          className={classes.textField}
          value={this.state.profile_photo}
          onChange={this.handleChange('profile_photo')}
          onClick={ (e) => { e.stopPropagation() } }
          margin="normal"
        />
        <TextField
          id="bioLine"
          label="Bio Line"
          className={classes.textField}
          value={this.state.bio_line}
          onChange={this.handleChange('bio_line')}
          onClick={ (e) => { e.stopPropagation() } }
          margin="normal"
        />
        <TextField
          required
          id="selectPrivacy"
          select
          label="Privacy"
          className={classes.textField}
          value={this.state.privacy_setting}
          onChange={this.handleChange('privacy_setting')}
          onClick={ (e) => { e.stopPropagation() } }
          SelectProps={{
            MenuProps: {
              className: classes.menu,
            },
          }}
          helperText="Please select privacy setting"
          margin="normal"
        >
          {privacySettings.map(option => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          required
          id="membershipPolicy"
          select
          label="Membership Policy"
          className={classes.textField}
          value={this.state.membership_policy}
          onChange={this.handleChange('membership_policy')}
          onClick={ (e) => { e.stopPropagation() } }
          SelectProps={{
            MenuProps: {
              className: classes.menu,
            },
          }}
          helperText="Please select membership policy"
          margin="normal"
        >
          {membershipPolicies.map(option => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </TextField>
        { saveButton() }
      </form>
    );  
  }
}

GroupForm.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(GroupForm);

