import React from "react"
import "../../genericStyles/_generic.scss"
import "./mainPage.scss"
import Title from "../../../components/UI-UX/title"
import MainPageLinks from "./module/mainPageLinks.jsx"
import { useSelector } from "react-redux"
import MainPageLinksAuth from "./module/mainPageLinksAuth"
import AuthPage100Vh from "../authpage100vh"
import Gradient from "../../../components/layouts/baseComponents/gradient"

function MainPage(props) {
	const user = useSelector((state) => state.user)

	const mainPage = (
		<>
			<div className="title_container title_container-main-page">
				<Title title={"Добро пожаловать!"} />
			</div>
			{user.isAuthenticated ? <MainPageLinksAuth /> : <MainPageLinks />}
		</>
	)

	return <AuthPage100Vh children={mainPage} />
}

export default MainPage
