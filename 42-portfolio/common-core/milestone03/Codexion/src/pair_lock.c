/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pair_lock.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:06:02 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	lock_second(t_coder *coder, int first, int second)
{
	int	result;
	int	rollback;

	if (first == second)
		return (1);
	result = pthread_mutex_lock(&coder->sim->dongles[second].mutex);
	if (!result)
		return (1);
	record_error(coder->sim, "pthread_mutex_lock(second dongle)", result);
	rollback = pthread_mutex_unlock(&coder->sim->dongles[first].mutex);
	if (rollback)
		record_error(coder->sim, "pthread_mutex_unlock(rollback)", rollback);
	sim_stop(coder->sim);
	return (0);
}

int	pair_lock(t_coder *coder)
{
	if (!coder_valid(coder))
		return (coder_error(coder, "dongle lock: invalid coder/index", EINVAL));
	return (pair_lock_validated(coder));
}

int	pair_lock_validated(t_coder *coder)
{
	int	first;
	int	second;
	int	result;

	first = coder->left;
	second = coder->right;
	if (first > second)
	{
		first = coder->right;
		second = coder->left;
	}
	result = pthread_mutex_lock(&coder->sim->dongles[first].mutex);
	if (result)
		return (sim_error(coder->sim, "pthread_mutex_lock(dongle)", result));
	return (lock_second(coder, first, second));
}

static int	unlock_dongle(t_coder *coder, int index)
{
	int	result;

	result = pthread_mutex_unlock(&coder->sim->dongles[index].mutex);
	if (result)
		return (sim_error(coder->sim,
				"pthread_mutex_unlock(dongle)", result));
	return (1);
}

int	pair_unlock(t_coder *coder)
{
	int	first;
	int	second;
	int	result;

	first = coder->left;
	second = coder->right;
	if (first > second)
	{
		first = coder->right;
		second = coder->left;
	}
	result = 1;
	if (first != second)
		result = unlock_dongle(coder, second);
	return (unlock_dongle(coder, first) && result);
}
