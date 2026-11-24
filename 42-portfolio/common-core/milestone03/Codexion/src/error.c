/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   error.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:32 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	record_error(t_sim *sim, const char *message, int code)
{
	if (!sim)
		return (boundary_error(message, code));
	if (!sim->error)
	{
		if (!message)
			message = "unspecified simulation failure";
		sim->failed = 1;
		sim->error_code = code;
		sim->error = message;
	}
	return (0);
}

int	sim_error(t_sim *sim, const char *message, int code)
{
	record_error(sim, message, code);
	if (sim)
		sim_stop(sim);
	return (0);
}

int	sim_lock(t_sim *sim)
{
	int	result;

	if (!sim || sim->sync_stage != 4 || sim->phase == SIM_EMPTY)
		return (boundary_error("coordinator: not initialized", EINVAL));
	result = pthread_mutex_lock(&sim->lock);
	if (result)
		return (boundary_error("pthread_mutex_lock(coordinator)", result));
	return (1);
}

int	sim_unlock(t_sim *sim)
{
	int	result;

	if (!sim || sim->sync_stage != 4 || sim->phase == SIM_EMPTY)
		return (boundary_error("coordinator: not initialized", EINVAL));
	result = pthread_mutex_unlock(&sim->lock);
	if (result)
		return (boundary_error("pthread_mutex_unlock(coordinator)", result));
	return (1);
}

int	sim_notify(t_sim *sim, int watch)
{
	int	result;

	if (!sim || sim->sync_stage != 4 || (watch != 0 && watch != 1))
		return (sim_error(sim, "notification: invalid context", EINVAL));
	if (watch)
		result = pthread_cond_signal(&sim->watch);
	else
		result = pthread_cond_broadcast(&sim->event);
	if (result)
		return (sim_error(sim, "pthread condition notification", result));
	return (1);
}
