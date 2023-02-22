import React, { useEffect } from "react"
import { useDispatch } from "react-redux"
import Authentication from "./api/authorization"
import { useNavigate } from "react-router-dom"
import { urls } from "../../urls"

function TokensCheck(props) {
	const dispatch = useDispatch()
	const navigate = useNavigate()

	function redirectLogin() {
		navigate(urls.login)
	}

	const refreshAccessToken = () => {
		new Authentication(dispatch).refreshToken(redirectLogin)
	}

	useEffect(() => {
		new Authentication(dispatch).refreshToken(redirectLogin)
		setInterval(refreshAccessToken, 1000 * 90)
	}, [])

	return <></>
}

export default TokensCheck
