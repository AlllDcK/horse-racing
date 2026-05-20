from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from core.use_cases.run_race import RunRaceUseCase
from core.services.odds_service import OddsService
from core.use_cases.place_bet import PlaceBetUseCase
from core.use_cases.deposit import DepositUseCase
from core.use_cases.withdraw import WithdrawUseCase
from core.use_cases.bet_history import BetHistoryUseCase


from .repositories import (
    HorseRepository,
    PlayerRepository,
    BetRepository
)


@login_required
def race_view(request):

    horse_repo = HorseRepository()
    player_repo = PlayerRepository()
    bet_repo = BetRepository()

    horses = horse_repo.get_all()

    player = player_repo.get_by_user(request.user)

    odds = OddsService.calculate(horses)
    odds_list = [(h, odds[h.id]) for h in horses]

    winner = None
    message = ""

    if request.method == "POST":

        try:
            horse_id = int(request.POST.get("horse_id"))
            amount = int(request.POST.get("amount"))
        except:
            return redirect('/')

        selected_horse = next(
            (h for h in horses if h.id == horse_id),
            None
        )

        if not selected_horse:
            return redirect('/')

        race = RunRaceUseCase()
        winner = race.execute(horses)

        bet_use_case = PlaceBetUseCase()

        try:

            result = bet_use_case.execute(
                player=player,
                selected_horse=selected_horse,
                winner=winner,
                amount=amount,
                odds=odds[selected_horse.id]
            )

        except Exception:
            return redirect('/')

        player_repo.save(request.user, result["player"])

        bet_repo.create(request.user, result["bet"])

        request.session['last_winner'] = winner.id

        return redirect('/')

    winner_id = request.session.pop('last_winner', None)

    if winner_id:

        winner = next(
            (h for h in horses if h.id == winner_id),
            None
        )

        message = "Результат гонки:"

    bet_history_use_case = BetHistoryUseCase()
    bets = bet_repo.get_user_bets(request.user)
    bets = bet_history_use_case.execute(bets)[:10]

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
        except:
            return redirect('/')

        player_repo = PlayerRepository()

        player = player_repo.get_by_user(request.user)

        use_case = DepositUseCase()

        try:
            player = use_case.execute(player, amount)
        except Exception:
            return redirect('/')

        player_repo.save(request.user, player)

    return redirect('/')


@login_required
def withdraw(request):

    if request.method == "POST":

        try:
            amount = int(request.POST.get("amount"))
        except:
            return redirect('/')

        player_repo = PlayerRepository()

        player = player_repo.get_by_user(request.user)

        use_case = WithdrawUseCase()

        try:
            player = use_case.execute(player, amount)
        except Exception:
            return redirect('/')

        player_repo.save(request.user, player)

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
