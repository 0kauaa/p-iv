"""visualização dos resultados do backtest.

gera figuras a partir dos arquivos salvos em `resultados/`:
  1. curvas acumuladas (riqueza relativa) de cada modelo
  2. drawdown ao longo do tempo
  3. retornos líquidos semanais dos modelos
  4. barras comparativas das métricas (acumulado, anualizado, Sharpe,
     Sortino, Max Drawdown)
  5. evolução dos pesos ao longo do tempo (por modelo)

as figuras são salvas em `resultados/graficos/`. para a evolução de pesos,
os pesos são recomputados via `backtest()` (não são persistidos em CSV).
"""

from pathlib import Path
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "modelagem"))

from backtest import backtest
PASTA_RESULTADOS = RAIZ / "resultados"
PASTA_GRAFICOS = PASTA_RESULTADOS / "graficos"

ARQUIVO_RETORNOS = PASTA_RESULTADOS / "retornos-backtest-agressivo.csv"
ARQUIVO_CURVAS = PASTA_RESULTADOS / "curvas-acumuladas-agressivo.csv"
ARQUIVO_METRICAS = PASTA_RESULTADOS / "tabela-metricas-agressivo.csv"
ARQUIVO_RETORNOS_PREP = RAIZ / "dados" / "prep" / "retornos-simples-semanais.csv"

PALETA = {
    "1/N": "#4C72B0",
    "shannon": "#DD8452",
    "tsallis": "#55A868",
    "renyi": "#C44E52",
    "wse": "#937860",
    "kl": "#8172B3",
}

ROTULOS_MODELOS = {
    "1/N": "1/N",
    "shannon": "Shannon",
    "tsallis": "Tsallis",
    "renyi": "Rényi",
    "wse": "WSE",
    "kl": "KL",
}


def _rotulo_modelo(nome):
    return ROTULOS_MODELOS.get(str(nome), str(nome))


def carregar_retornos(arquivo=ARQUIVO_RETORNOS):
    return pd.read_csv(arquivo, index_col="Date", parse_dates=True)


def carregar_curvas(arquivo=ARQUIVO_CURVAS):
    return pd.read_csv(arquivo, index_col="Date", parse_dates=True)


def carregar_metricas(arquivo=ARQUIVO_METRICAS):
    return pd.read_csv(arquivo, index_col=0)


def _estilo():
    mpl.rcParams.update(
        {
            "figure.dpi": 120,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "font.size": 10,
            "axes.formatter.use_locale": False,
        }
    )


def _eixo_x_datas(ax):
    """deixa o eixo temporal legível: um rótulo por ano, sem sobreposição."""
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.margins(x=0)


def _eixo_y_percentual(ax, decimais=0):
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=decimais))


def grafico_curvas(curvas, arquivo):
    """curvas acumuladas (riqueza) por modelo em escala log2 com rótulos simples."""
    fig, ax = plt.subplots(figsize=(10, 5))
    for col in curvas.columns:
        ax.plot(curvas.index, curvas[col], label=_rotulo_modelo(col), color=PALETA[col], lw=1.6)
    ax.axhline(1.0, color="black", lw=0.8, alpha=0.5, ls="--")
    ax.set_yscale("log", base=2)
    ax.yaxis.set_major_locator(mticker.LogLocator(base=2))
    ax.yaxis.set_minor_locator(mticker.NullLocator())
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:g}×"))
    ax.set_title("Evolução acumulada do portfólio")
    ax.set_xlabel("Data")
    ax.set_ylabel("Riqueza relativa ao início ($t_0 = 1$)")
    ax.grid(True, which="major", alpha=0.3)
    _eixo_x_datas(ax)
    ax.legend(ncol=3, loc="upper left")
    fig.tight_layout()
    fig.savefig(arquivo, bbox_inches="tight")
    plt.close(fig)
    print(f"salvo em {arquivo}")


def grafico_drawdown(curvas, arquivo):
    """drawdown acumulado por modelo (área abaixo de zero)."""
    fig, ax = plt.subplots(figsize=(10, 5))
    for col in curvas.columns:
        dd = curvas[col] / curvas[col].cummax() - 1.0
        ax.plot(curvas.index, dd, label=_rotulo_modelo(col), color=PALETA[col], lw=1.4)
    ax.axhline(0.0, color="black", lw=0.8, alpha=0.5)
    ax.set_title("Drawdown acumulado por modelo")
    ax.set_xlabel("Data")
    ax.set_ylabel("Queda em relação ao pico")
    _eixo_y_percentual(ax)
    _eixo_x_datas(ax)
    ax.legend(ncol=6, loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False)
    fig.tight_layout()
    fig.savefig(arquivo, bbox_inches="tight")
    plt.close(fig)
    print(f"salvo em {arquivo}")


def grafico_retornos(retornos, arquivo):
    """retornos líquidos semanais por modelo (barra discreta)."""
    fig, ax = plt.subplots(figsize=(10, 5))
    for col in retornos.columns:
        ax.plot(retornos.index, retornos[col], label=_rotulo_modelo(col), color=PALETA[col], lw=0.8)
    ax.axhline(0.0, color="black", lw=0.8, alpha=0.5)
    ax.set_title("Retornos líquidos semanais por modelo")
    ax.set_xlabel("Data")
    ax.set_ylabel("Retorno semanal")
    _eixo_y_percentual(ax)
    _eixo_x_datas(ax)
    ax.legend(ncol=6, loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False)
    fig.tight_layout()
    fig.savefig(arquivo, bbox_inches="tight")
    plt.close(fig)
    print(f"salvo em {arquivo}")


ROTULOS_METRICAS = {
    "retorno_acumulado": ("Retorno acumulado", True),
    "retorno_anualizado": ("Retorno anualizado", True),
    "vol_anual": ("Volatilidade anual", True),
    "sharpe": ("Sharpe", False),
    "sortino": ("Sortino", False),
    "max_drawdown": ("Drawdown máximo", True),
}


def grafico_metricas(metricas, arquivo):
    """barras comparativas das métricas de cada modelo."""
    metricas_t = metricas.T
    n = len(metricas)
    linhas = int(np.ceil(n / 3))

    fig, axes = plt.subplots(linhas, 3, figsize=(12, 4 * linhas))
    axes = np.atleast_1d(axes).ravel()

    for i, (metrica, valores) in enumerate(metricas_t.iterrows()):
        ax = axes[i]
        cores = [PALETA[nome] for nome in metricas_t.columns]
        ax.bar(metricas_t.columns, valores, color=cores)
        ax.axhline(0.0, color="black", lw=0.8, alpha=0.5)
        rotulo, percentual = ROTULOS_METRICAS.get(metrica, (metrica, False))
        ax.set_title(rotulo)
        ax.set_ylabel("Percentual" if percentual else "Valor")
        if percentual:
            _eixo_y_percentual(ax)
        ax.set_xticks(range(len(metricas_t.columns)))
        ax.set_xticklabels(
            [_rotulo_modelo(nome) for nome in metricas_t.columns], rotation=30, ha="right"
        )
        ax.margins(x=0.02)

    for j in range(n, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("Métricas de desempenho por modelo", y=1.0)
    fig.tight_layout()
    fig.savefig(arquivo, bbox_inches="tight")
    plt.close(fig)
    print(f"salvo em {arquivo}")


def grafico_pesos(pesos_series, arquivo):
    """evolução dos pesos por modelo (áreas empilhadas)."""
    n = len(pesos_series)
    cols = list(next(iter(pesos_series.values())).columns)
    colunas = int(np.ceil(np.sqrt(n)))

    fig, axes = plt.subplots(
        n // colunas + (n % colunas > 0), colunas, figsize=(14, 3.2 * (1 + n // colunas))
    )
    axes = np.atleast_1d(axes).ravel()

    for i, (nome, pesos) in enumerate(pesos_series.items()):
        ax = axes[i]
        ax.stackplot(pesos.index, pesos.T, labels=cols, alpha=0.85)
        ax.set_title(_rotulo_modelo(nome))
        ax.set_ylim(0, 1)
        _eixo_y_percentual(ax)
        _eixo_x_datas(ax)
        if i % colunas == 0:
            ax.set_ylabel("Peso (%)")
        if i >= n - colunas:
            ax.set_xlabel("Data")

    for j in range(n, len(axes)):
        axes[j].set_visible(False)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=len(cols), frameon=True)
    fig.suptitle("Evolução dos pesos por modelo", y=1.0)
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.08)
    fig.savefig(arquivo, bbox_inches="tight")
    plt.close(fig)
    print(f"salvo em {arquivo}")


CENARIOS = {
    # sufixo de arquivo -> (rótulo, fator_var usado para recomputar os pesos).
    "-agressivo": ("agressivo", 2.0),
    "-conservador": ("conservador", 1.0),
}


def gerar_todos(sufixo="-agressivo"):
    """gera todas as figuras de um cenário a partir dos arquivos de `resultados/`."""
    PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

    retornos = pd.read_csv(PASTA_RESULTADOS / f"retornos-backtest{sufixo}.csv", index_col="Date", parse_dates=True)
    curvas = pd.read_csv(PASTA_RESULTADOS / f"curvas-acumuladas{sufixo}.csv", index_col="Date", parse_dates=True)
    metricas = pd.read_csv(PASTA_RESULTADOS / f"tabela-metricas{sufixo}.csv", index_col=0)

    grafico_curvas(curvas, PASTA_GRAFICOS / f"curvas-acumuladas{sufixo}.png")
    grafico_drawdown(curvas, PASTA_GRAFICOS / f"drawdown{sufixo}.png")
    grafico_retornos(retornos, PASTA_GRAFICOS / f"retornos-semanais{sufixo}.png")
    grafico_metricas(metricas, PASTA_GRAFICOS / f"metricas{sufixo}.png")

    _, pesos_series = backtest(
        pd.read_csv(ARQUIVO_RETORNOS_PREP, index_col="Date", parse_dates=True),
        fator_var=CENARIOS[sufixo][1],
    )
    grafico_pesos(pesos_series, PASTA_GRAFICOS / f"pesos{sufixo}.png")


def gerar_cenarios():
    """gera as figuras dos dois cenários (agressivo + conservador)."""
    for sufixo, (rotulo, _) in CENARIOS.items():
        print(f"===== cenário {rotulo} (sufixo={sufixo}) =====")
        gerar_todos(sufixo)


if __name__ == "__main__":
    _estilo()
    gerar_cenarios()