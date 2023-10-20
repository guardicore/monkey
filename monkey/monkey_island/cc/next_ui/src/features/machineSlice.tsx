import {createSlice} from '@reduxjs/toolkit'
import authFetch from '@/utils/common/authFetch';

export const machineSlice = createSlice({
  name: 'machines',
  initialState: {
    machines: []
  },
  reducers: {
    set: (state, action) => {
        state.machines = action.payload
    },
  }
})

export const { set } = machineSlice.actions

export const fetchMachines = () => async dispatch => {
    await authFetch('/api/machines', {'method': 'GET'})
        .then(res => res.json())
        .then(data => {
            dispatch(set(data))
        })
}

export const selectMachines = state => state.machines.machines
export const machineById = (state, id) => state.machines.machines.find(machine =>
    Number(machine.id) === Number(id)
)


export default machineSlice.reducer
