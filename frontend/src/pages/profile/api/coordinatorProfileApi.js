import { getAxiosInstanceAuth } from "../../../actions/axios_config"

export class CoordinatorInfo {
	constructor(dispatch) {
		this.dispatch = dispatch
	}

	async getCoordinatorInfo() {
		const axiosInstanceAuth = getAxiosInstanceAuth()

		return await axiosInstanceAuth.get("api/coordinator/retrieve").then((response) => {
			if (response.status === 200) {
				this.dispatch({
					type: "SET_COORDINATOR",
					payload: response.data,
				})
			}
			return response
		})
	}

	async getInviteCode() {
		const axiosInstanceAuth = getAxiosInstanceAuth()

		return await axiosInstanceAuth
			.get("api/coordinator/invite-code")
			.then((response) => {
				return response
			})
			.catch((reason) => {
				return reason
			})
	}

	async updateInviteCode() {
		const axiosInstanceAuth = getAxiosInstanceAuth()

		return await axiosInstanceAuth
			.put("api/coordinator/invite-code")
			.then((response) => {
				return response
			})
			.catch((reason) => {
				return reason
			})
	}
}
