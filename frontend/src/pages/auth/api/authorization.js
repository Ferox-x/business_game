import { axiosInstance, axiosRefresh } from "../../../actions/axios_config"
import { NoticeApiBase } from "../../../utilits/baseApiClasses"

class Authentication extends NoticeApiBase {
	#setUser(role) {
		if (role === "Player") {
			this.dispatch({
				type: "SET_PLAYER",
				payload: {},
			})
		}
		if (role === "Coordinator") {
			this.dispatch({
				type: "SET_COORDINATOR",
				payload: {},
			})
		}
	}

	async registration(email, password, invite_code) {
		return await axiosInstance
			.post("api/signup/", {
				user: {
					email,
					password,
					invite_code,
				},
			})
			.then((response) => {
				if (response.status === 201) {
					this.createNoticeSuccess("Вы успешно зарегистрировались!")
					this.createNoticeSuccess("Пожалуйста войдите.")
				}
				return response
			})
			.catch((response) => {
				const errors = response.response.data.errors
				this.createNoticeError(errors)
				return response
			})
	}

	async refreshToken(redirect) {
		const refreshToken = localStorage.getItem("refreshToken")
		if (!refreshToken) {
			return null
		}
		return await axiosRefresh
			.post("api/refresh/", { refreshToken })
			.then((response) => {
				if (response.status === 200) {
					localStorage.setItem("accessToken", response.data.access_token)
				}
				return response
			})
			.catch((response) => {
				this.createNoticeError(["Ваша сессия истекла, пожалуйста войдите."])
				redirect()
			})
	}

	async login(email, password) {
		return await axiosInstance
			.post("api/login/", {
				user: {
					email,
					password,
				},
			})
			.then((response) => {
				if (response.status === 200) {
					this.createNoticeSuccess("Вы успешно вошли.")
					const accessToken = response.data.access_token
					const refreshToken = response.data.refresh_token
					const role = response.data.role
					localStorage.setItem("accessToken", accessToken)
					localStorage.setItem("refreshToken", refreshToken)
					this.#setUser(role)
				}
				return response
			})
			.catch((response) => {
				const errors = response.response.data.errors
				this.createNoticeError(errors)
				return response
			})
	}
}

export default Authentication
