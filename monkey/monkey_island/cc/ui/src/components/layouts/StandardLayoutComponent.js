import React from "react"
import {Route} from "react-router-dom"
import SideNavComponent from "../SideNavComponent"

export const StandardLayoutComponent = ({component: Component, ...rest}) => (
  <Route {...rest} render={() => (
    <>
      <SideNavComponent completedSteps={rest['completedSteps']}/>
      <Component {...rest} />
    </>
  )}/>
)
