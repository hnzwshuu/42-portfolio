/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:21 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	finish_compile(t_coder *coder)
{
	t_sim	*sim;

	sim = coder->sim;
	if (!release_pair(coder))
		return (0);
	if (!sim_live(sim))
		return (0);
	if (coder->completed < sim->conf.required)
		coder->completed++;
	if (!coder->finished && coder->completed == sim->conf.required)
	{
		coder->finished = 1;
		sim->finished_count++;
	}
	if (sim->finished_count == sim->conf.count)
	{
		sim_stop(sim);
		return (0);
	}
	return (1);
}

static int	idle_phases(t_coder *coder)
{
	t_sim	*sim;
	t_time	at;

	sim = coder->sim;
	at = coder->released_at;
	log_state(coder, "is debugging", at);
	if (!pause_until(sim, deadline_after(sim, at, sim->conf.debug)))
		return (0);
	at = now_us(sim);
	log_state(coder, "is refactoring", at);
	return (pause_until(sim, deadline_after(sim, at, sim->conf.refactor)));
}

static int	coder_cycle(t_coder *coder)
{
	t_sim	*sim;

	sim = coder->sim;
	if (!coder_state_valid(coder) || coder->sim->finished_count < 0
		|| coder->sim->finished_count > coder->sim->capacity)
		return (coder_error(coder, "cycle: invalid coder state", EINVAL));
	if (!coder->queued && !queue_request(coder))
		return (0);
	if (!acquire_pair(coder))
		return (0);
	if (!pause_until(sim,
			deadline_after(sim, coder->last_start, sim->conf.compile)))
	{
		release_pair(coder);
		return (0);
	}
	if (!finish_compile(coder))
		return (0);
	return (idle_phases(coder));
}

static void	yield_empty_cycle(t_sim *sim)
{
	if (sim->conf.compile + sim->conf.debug + sim->conf.refactor
		+ sim->conf.cooldown == 0)
		wait_until(sim, &sim->event, deadline_after(sim, now_us(sim), 100));
}

void	coder_loop(t_coder *coder)
{
	if (!coder_state_valid(coder))
	{
		coder_error(coder, "coder loop: invalid context", EINVAL);
		return ;
	}
	while (sim_live(coder->sim) && coder_cycle(coder))
		yield_empty_cycle(coder->sim);
}
