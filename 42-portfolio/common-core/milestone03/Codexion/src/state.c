/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   state.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:06:17 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	find_expired(t_sim *sim, t_time now)
{
	int	index;
	int	earliest;

	earliest = 0;
	index = 0;
	while (index < sim->conf.count)
	{
		if (sim->coders[index].last_start < 0
			|| sim->coders[index].last_start > now)
		{
			sim_error(sim, "burnout check: invalid compile timestamp", index);
			return (-2);
		}
		if (sim->coders[index].last_start < sim->coders[earliest].last_start)
			earliest = index;
		index++;
	}
	if (now - sim->coders[earliest].last_start >= sim->conf.burnout)
		return (earliest);
	return (-1);
}

int	expired_coder(t_sim *sim, t_time now)
{
	if (!sim_valid(sim) || now < 0)
	{
		sim_error(sim, "burnout check: invalid simulation or time", EINVAL);
		return (-2);
	}
	return (find_expired(sim, now));
}

int	sim_live(t_sim *sim)
{
	if (!sim_valid(sim))
		return (sim_error(sim, "liveness: invalid simulation", EINVAL));
	return (sim_active(sim));
}

int	sim_active(t_sim *sim)
{
	int		index;
	t_time	now;

	if (sim->stopped)
		return (0);
	if (sim->phase != SIM_RUNNING || !sim->ready)
		return (sim_error(sim, "liveness: simulation not started", EINVAL));
	now = now_us(sim);
	if (now < 0)
		return (0);
	index = find_expired(sim, now);
	if (index != -1)
	{
		if (index >= 0)
			sim_notify(sim, 1);
		return (0);
	}
	return (1);
}

int	wait_ready(t_sim *sim)
{
	if (!sim_valid(sim) || sim->phase != SIM_RUNNING)
		return (sim_error(sim, "start barrier: invalid lifecycle", EINVAL));
	while (!sim->ready && !sim->stopped)
		wait_event(sim);
	return (!sim->stopped);
}
