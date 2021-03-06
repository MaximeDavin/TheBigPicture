import React from 'react'
import { Route } from 'react-router-dom'

import Home from '../pages/Home'
import BigPictureView from '../pages/BigPicture'
import RatingView from '../pages/Rating'
import UserView from '../pages/User'
import NavBar from '../NavBar'
import Api from '../Api'
import Executor from '../Api/executor'
import NotificationManager from '../../components/NotificationManager'
import './style.scss'

const App = () => (
  <div>
    <NavBar />
    <div id="routes">
      <Route exact={true} path="/subject/:subjectId/bigPicture/:bpId" component={BigPictureView} />
      <Route exact={true} path="/subject/:subjectId/rating/:ratingId" component={RatingView} />
      <Route exact={true} path="/user/:id" component={UserView} />
      <Route exact={true} path="/" component={Home}/>
    </div>
    <NotificationManager />
    <Api />
    <Executor />
  </div>
)

export default App
