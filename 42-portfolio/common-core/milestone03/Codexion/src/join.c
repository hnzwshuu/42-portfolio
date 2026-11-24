/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   join.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:43 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	join_result(t_sim *sim, int code, void *result, int monitor)
{
	if (!sim_lock(sim))
		return (0);
	if (code)
		sim_error(sim, "pthread_join", code);
	else
	{
		if (monitor)
			sim->monitor_created = 0;
		else
			sim->created--;
		if (result)
			sim_error(sim, "thread returned failure", 0);
	}
	if (!sim_unlock(sim))
		return (0);
	return (code == 0);
}

static int	join_coders(t_sim *sim)
{
	void	*result;
	int		code;

	while (sim->created > 0)
	{
		result = NULL;
		code = pthread_join(sim->coders[sim->created - 1].thread, &result);
		if (!join_result(sim, code, result, 0))
			return (0);
	}
	return (1);
}

static int	join_monitor(t_sim *sim)
{
	void	*result;
	int		code;

	if (!sim->monitor_created)
		return (1);
	result = NULL;
	code = pthread_join(sim->monitor, &result);
	return (join_result(sim, code, result, 1));
}

int	sim_join(t_sim *sim)
{
	if (!sim_valid(sim)
		|| (sim->phase != SIM_RUNNING && sim->phase != SIM_DONE)
		|| sim->created < 0 || sim->created > sim->capacity
		|| (sim->monitor_created != 0 && sim->monitor_created != 1)
		|| (sim->phase == SIM_DONE
			&& (sim->created || sim->monitor_created)))
		return (boundary_error("sim_join: invalid state", 0));
	if (!join_coders(sim) || !join_monitor(sim))
		return (0);
	sim->phase = SIM_DONE;
	return (1);
}
