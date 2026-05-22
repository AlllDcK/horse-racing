from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from core.services.odds_service import OddsService
from core.use_cases.factory import UseCaseFactory


@login_required
def race_view(request):

    horse_repo = UseCaseFactory.horse_repo()
    horses = horse_repo.get_all()

    odds = OddsService.calculate(horses)
    odds_list = [(h, odds[h.id]) for h in horses]

    winner = None
    message = ""

    if request.method == "POST":
        try:
            horse_id = int(request.POST.get("horse_id"))
            amount = int(request.POST.get("amount"))
        except (TypeError, ValueError):
            return redirect('/')

        selected_horse = next(
            (h for h in horses if h.id == horse_id), None
        )

        if not selected_horse:
            return redirect('/')

        winner = UseCaseFactory.run_race().execute(horses)

        try:
            UseCaseFactory.place_bet().execute(
                user=request.user,
                selected_horse=selected_horse,
                winner=winner,
                amount=amount,
                odds=odds[selected_horse.id]
            )
        except Exception:
            return redirect('/')

        request.session['last_winner'] = winner.id
        return redirect('/')

    winner_id = request.session.pop('last_winner', None)
    if winner_id:
        winner = next((h for h in horses if h.id == winner_id), None)
        message = "Результат гонки:"

    bet_repo = UseCaseFactory.bet_repo()
    raw_bets = bet_repo.get_user_bets(request.user)
    bets = UseCaseFactory.bet_history().execute(raw_bets)[:10]

    player = UseCaseFactory.player_repo().get_by_user(request.user)

    return render(request, "races/race.html", {
        "horses": horses,
        "winner": winner,
        "winner_id": winner.id if winner else None,
        "message": message,
        "balance": player.balance,
        "odds_list": odds_list,
        "bets": bets
    })


@login_required
def deposit(request):
    if request.method == "POST":
        try:
            amount = int(request.POST.get("amount"))
        except (TypeError, ValueError):
            return redirect('/')

        try:
            UseCaseFactory.deposit().execute(request.user, amount)
        except Exception:
            return redirect('/')

    return redirect('/')


@login_required
def withdraw(request):
    if request.method == "POST":
        try:
            amount = int(request.POST.get("amount"))
        except (TypeError, ValueError):
            return redirect('/')

        try:
            UseCaseFactory.withdraw().execute(request.user, amount)
        except Exception:
            return redirect('/')

    return redirect('/')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})