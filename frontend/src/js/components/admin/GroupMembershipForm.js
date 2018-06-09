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

const adminValues = [
  {
    id: 'true',
    name: 'Yes'
  },
  {
    id: 'false',
    name: 'No'
  }
]

const typeValues = [
  {
    id: 'ephemeral',
    name: 'Ephemeral'
  },
  {
    id: 'primary',
    name: 'Primary'
  }
]

class GroupMembershipForm extends React.Component {
  state = { ...this.props.membership, changed: this.props.membership.changed || false };

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
    } else {
      this.setState({ ...this.props.membership, changed: false })
    }
  }

  handleDelete(e) {
    e.preventDefault();
    this.props.onDelete(this.state);
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
    const deleteButton = function() {
      if (this.state.id !== 'unsaved') { 
        return (
          <button onClick={ (e) => { e.stopPropagation(); this.handleDelete(e); } } className="btn btn-danger btn-sm">delete</button>
        )
      }
    }.bind(this)
    const drinkerSuggestions = this.props.drinkerSuggestions[this.state.type].concat(this.props.drinkerSuggestions.open)
    // Need to offer the current drinker as a suggestion if it isn't currently shown
    const referencedDrinker = this.state.changed ? this.props.drinkerSuggestions.all[this.props.membership.drinker_id] : this.props.drinkerSuggestions.all[this.state.drinker_id]
    if (referencedDrinker && !drinkerSuggestions.includes(referencedDrinker)) drinkerSuggestions.push(referencedDrinker);

    return (
      <form className={classes.container} 
            onKeyPress={(e) => { if (e.key === 'Enter') e.preventDefault(); return; }} 
            onSubmit={(e) => { this.handleSubmit(e); }} 
            autoComplete="off">
        <TextField
          required
          id="drinker"
          select
          label="Drinker"
          className={classes.textField}
          value={this.state.drinker_id}
          onChange={this.handleChange('drinker_id')}
          onClick={ (e) => { e.stopPropagation() } }
          SelectProps={{
            MenuProps: {
              className: classes.menu,
            },
          }}
          margin="normal"
        >
          {drinkerSuggestions.map(option => (
            <MenuItem key={option.id} value={option.id}>
              {option.name}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          hidden
          id="group"
          select
          label="Group"
          className={classes.textField}
          value={this.state.group_id}
          onClick={ (e) => { e.stopPropagation() } }
          SelectProps={{
            MenuProps: {
              className: classes.menu,
            },
          }}
          margin="normal"
        >
          {[{id: this.state.group_id, name: this.props.group.name}].map(option => (
            <MenuItem key={option.id} value={option.id}>
              {option.name}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          required
          id="isAdmin"
          select
          label="Is Admin"
          className={classes.textField}
          value={this.state.admin.toString()}
          onChange={this.handleChange('admin')}
          onClick={ (e) => { e.stopPropagation() } }
          SelectProps={{
            MenuProps: {
              className: classes.menu,
            },
          }}
          margin="normal"
        >
          {adminValues.map(option => (
            <MenuItem key={option.id} value={option.id}>
              {option.name}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          required
          id="type"
          select
          label="Membership Type"
          className={classes.textField}
          value={this.state.type}
          onChange={this.handleChange('type')}
          onClick={ (e) => { e.stopPropagation() } }
          SelectProps={{
            MenuProps: {
              className: classes.menu,
            },
          }}
          helperText="Membership Type"
          margin="normal"
        >
          {typeValues.map(option => (
            <MenuItem key={option.id} value={option.id}>
              {option.name}
            </MenuItem>
          ))}
        </TextField>
        { saveButton() }
        { deleteButton() }
      </form>
    );  
  }
}

GroupMembershipForm.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(GroupMembershipForm);
