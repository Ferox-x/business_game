import { useDispatch, useSelector } from "react-redux"
import { useNavigate } from "react-router-dom"
import React, { useEffect } from "react"
import { NoticeService } from "../services/noticeService"
import { urls } from "../urls"
import Error403 from "./errors/error403"

export function RequireAuthPlayer({ children, ...props }) {
	let user = useSelector((state) => state.user)
	const dispatch = useDispatch()
	const navigate = useNavigate()

	useEffect(() => {
		if (!user.isAuthenticated) {
			new NoticeService(dispatch).addErrorNotice("Пожалуйста, войдите.")
			navigate(urls.mainPage)
		}
	}, [])

	if (user.isPlayer) {
		return children
	}
	return <Error403 />
}

export function RequireAuthCoordinator({ children, ...props }) {
	let user = useSelector((state) => state.user)
	const dispatch = useDispatch()
	const navigate = useNavigate()

	useEffect(() => {
		if (!user.isAuthenticated) {
			new NoticeService(dispatch).addErrorNotice("Пожалуйста, войдите.")
			navigate(urls.mainPage)
		}
	}, [])

	if (user.isCoordinator) {
		return children
	}
	return <Error403 />
}

export function useCheckPLayer(children) {
	let user = useSelector((state) => state.user)

	if (user.isPlayer) {
		return true
	}
	return false
}

export function useCheckCoordinator(children) {
	let user = useSelector((state) => state.user)

	if (user.isCoordinator) {
		return true
	}
	return false
}
