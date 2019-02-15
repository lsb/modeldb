import { IFilterData } from 'models/Filters';
import { ActionResult } from 'store/store';
import { action } from 'typesafe-actions';
import ServiceFactory from '../../services/ServiceFactory';
import { fetchProjectsAction, fetchProjectsActionTypes } from './types';

export const fetchProjects = (filters?: IFilterData[]): ActionResult<void, fetchProjectsAction> => async (dispatch, getState) => {
  dispatch(action(fetchProjectsActionTypes.FETCH_PROJECTS_REQUEST));

  await ServiceFactory.getProjectsService()
    .getProjects(filters)
    .then(res => {
      dispatch(action(fetchProjectsActionTypes.FETCH_PROJECTS_SUCCESS, res));
    })
    .catch(err => {
      dispatch(action(fetchProjectsActionTypes.FETCH_PROJECTS_REQUEST));
    });
};
