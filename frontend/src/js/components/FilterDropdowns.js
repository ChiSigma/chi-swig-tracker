/* eslint-disable react/prop-types */

import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Input from '@material-ui/core/Input';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import CancelIcon from '@material-ui/icons/Cancel';
import ArrowDropUpIcon from '@material-ui/icons/ArrowDropUp';
import ClearIcon from '@material-ui/icons/Clear';
import Chip from '@material-ui/core/Chip';
import Select from 'react-select';
import 'react-select/dist/react-select.css';

const profileTypes = [
  { label: 'Drinkers', value: 'drinkers' },
  { label: 'Groups', value: 'groups' }
];

class Option extends React.Component {
  handleClick = event => {
    this.props.onSelect(this.props.option, event);
  };

  render() {
    const { children, isFocused, isSelected, onFocus } = this.props;

    return (
      <MenuItem
        onFocus={onFocus}
        selected={isFocused}
        onClick={this.handleClick}
        component="div"
        style={{
          fontWeight: isSelected ? 500 : 400,
        }}
      >
        {children}
      </MenuItem>
    );
  }
}

function SelectWrapped(props) {
  const { classes, ...other } = props;

  return (
    <Select
      optionComponent={Option}
      noResultsText={<Typography>{'No results found'}</Typography>}
      arrowRenderer={arrowProps => {
        return arrowProps.isOpen ? <ArrowDropUpIcon /> : <ArrowDropDownIcon />;
      }}
      clearRenderer={() => <ClearIcon />}
      valueComponent={valueProps => {
        const { value, children, onRemove } = valueProps;

        const onDelete = event => {
          event.preventDefault();
          event.stopPropagation();
          onRemove(value);
        };

        if (onRemove) {
          return (
            <Chip
              tabIndex={-1}
              label={children}
              className={classes.chip}
              deleteIcon={<CancelIcon onTouchEnd={onDelete} />}
              onDelete={onDelete}
            />
          );
        }

        return <div className="Select-value">{children}</div>;
      }}
      {...other}
    />
  );
}

const ITEM_HEIGHT = 48;

const styles = theme => ({
  root: {
    flexGrow: 1,
    height: 250,
  },
  chip: {
    margin: theme.spacing.unit / 4,
  },
  // We had to use a lot of global selectors in order to style react-select.
  // We are waiting on https://github.com/JedWatson/react-select/issues/1679
  // to provide a much better implementation.
  // Also, we had to reset the default style injected by the library.
  '@global': {
    '.Select-control': {
      display: 'flex',
      alignItems: 'center',
      border: 0,
      height: 'auto',
      background: 'transparent',
      '&:hover': {
        boxShadow: 'none',
      },
    },
    '.Select-multi-value-wrapper': {
      flexGrow: 1,
      display: 'flex',
      flexWrap: 'wrap',
    },
    '.Select--multi .Select-input': {
      margin: 0,
    },
    '.Select.has-value.is-clearable.Select--single > .Select-control .Select-value': {
      padding: 0,
    },
    '.Select-noresults': {
      padding: theme.spacing.unit * 2,
    },
    '.Select-input': {
      display: 'inline-flex !important',
      padding: 0,
      height: 'auto',
    },
    '.Select-input input': {
      background: 'transparent',
      border: 0,
      padding: 0,
      cursor: 'default',
      display: 'inline-block',
      fontFamily: 'inherit',
      fontSize: 'inherit',
      margin: 0,
      outline: 0,
    },
    '.Select-placeholder, .Select--single .Select-value': {
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      display: 'flex',
      alignItems: 'center',
      fontFamily: theme.typography.fontFamily,
      fontSize: theme.typography.pxToRem(16),
      padding: 0,
    },
    '.Select-placeholder': {
      opacity: 0.42,
      color: theme.palette.common.black,
    },
    '.Select-menu-outer': {
      backgroundColor: theme.palette.background.paper,
      boxShadow: theme.shadows[2],
      position: 'absolute',
      left: 0,
      top: `calc(100% + ${theme.spacing.unit}px)`,
      width: '100%',
      zIndex: 2,
      maxHeight: ITEM_HEIGHT * 4.5,
    },
    '.Select.is-focused:not(.is-open) > .Select-control': {
      boxShadow: 'none',
    },
    '.Select-menu': {
      maxHeight: ITEM_HEIGHT * 4.5,
      overflowY: 'auto',
    },
    '.Select-menu div': {
      boxSizing: 'content-box',
      zIndex: 999
    },
    '.Select-arrow-zone, .Select-clear-zone': {
      color: theme.palette.action.active,
      cursor: 'pointer',
      height: 21,
      width: 21,
      zIndex: 1,
    },
    // Only for screen readers. We can't use display none.
    '.Select-aria-only': {
      position: 'absolute',
      overflow: 'hidden',
      clip: 'rect(0 0 0 0)',
      height: 1,
      width: 1,
      margin: -1,
    },
  },
});

class FilterDropdowns extends React.Component {
  constructor(props) {
    super(props);

    this.cache = () => { return this.props.context.cache };
    this.appState = () => { return this.props.context.state };
    this.state = { ...props.state, drinkersSuggested: [], groupsSuggested: [] };
  }

  handleChange = function(name) {
    return async (value) => {
      this.props.updateParent({
        [name]: value,
      });
      this.props.updateParent({ loading: true })
      const selectedGroups = name === 'groups' ? value : this.state.groups;
      const selectedDrinkers = name === 'drinkers' ? value : this.state.drinkers;
      const profileType = name === 'profileType' ? value : this.state.profileType;
      await this.updateSuggestions(profileType, selectedGroups, selectedDrinkers);
    }
  };

  async componentWillMount() {
    this.props.updateParent({ loading: true })
    await this.updateSuggestions();
  }

  async updateSuggestions(profileType=this.state.profileType, selectedGroups=this.state.groups, selectedDrinkers=this.state.drinkers) {
    // Calling fucntions first so both requests fire and then I await them
    let drinkers = this.cache().fetchFilterSuggestions('drinkers', selectedGroups, selectedDrinkers);
    let groups = this.cache().fetchFilterSuggestions('groups', selectedGroups, selectedDrinkers);
    let version = this.appState().checkVersion({ profileType, groups: selectedGroups, drinkers: selectedDrinkers })
    drinkers = await drinkers;
    groups = await groups;
    version = await version;

    this.setState({ profileType, groups: selectedGroups, drinkers: selectedDrinkers,
                    drinkersSuggested: drinkers.map(drinker => ({
                                        value: drinker.id,
                                        label: drinker.name,
                    })),
                    groupsSuggested: groups.map(group => ({
                                      value: group.id,
                                      label: group.name
                    }))
    });
    this.props.updateParent({ loading: false, version: version })
  }

  render() {
    const { classes } = this.props;

    const groupFilter = this.state.profileType === 'drinkers' ? (
                <Input
                  fullWidth
                  inputComponent={SelectWrapped}
                  value={this.state['groups']}
                  onChange={this.handleChange('groups')}
                  placeholder="Filter by Groups"
                  name="react-select-groups"
                  inputProps={{
                    classes,
                    multi: true,
                    instanceId: 'react-select-groups',
                    id: 'react-select-groups',
                    simpleValue: true,
                    options: this.state.groupsSuggested,
                    required: true
                  }}
                />
            ) : (
                console.log('showing groups - no group filter')
            );

    return (
      <div className={classes.root}>
        <Input
          fullWidth
          inputComponent={SelectWrapped}
          value={this.state.profileType}
          onChange={this.handleChange('profileType')}
          placeholder="Select a Profile Type"
          name="react-select-single"
          inputProps={{
            classes,
            name: 'react-select-single',
            instanceId: 'react-select-single',
            id: 'react-select-single',
            simpleValue: true,
            clearable: false,
            options: profileTypes
          }}
        />
        { groupFilter }
        <Input
          fullWidth
          inputComponent={SelectWrapped}
          value={this.state[this.state.profileType]}
          onChange={this.handleChange(this.state.profileType)}
          placeholder={"Filter by " + this.state.profileType}
          name="react-select-ids"
          inputProps={{
            classes,
            multi: true,
            instanceId: 'react-select-ids',
            id: 'react-select-ids',
            simpleValue: true,
            options: this.state[this.state.profileType + 'Suggested'],
          }}
        />
      </div>
    );
  }
}

FilterDropdowns.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(FilterDropdowns);