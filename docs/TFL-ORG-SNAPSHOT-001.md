# TFL-ORG-SNAPSHOT-001

## Relational Organization as State

**Datum:** 2026-08-18  
**Status:** Working Research Anchor / Pre-Codex Re-evaluation  
**Bezug:** TFL / RDL / Aerlis-UAS / SPATIAL Orientation

## 1. Zentrale Erkenntnis

Die bisherige TFL/RDL-Beobachtungsbasis hat möglicherweise teilweise die **sichtbare geometrische Realisierung** mit dem eigentlichen **Organisationszustand** gleichgesetzt.

Positionen, Bewegungsvektoren, Abstände, Winkel und Formation beschreiben

\[
X_{\mathrm{geometry}}(t)
\]

aber nicht zwingend den zugrunde liegenden Zustand

\[
Z_{\mathrm{organization}}(t).
\]

Neue Arbeitshypothese:

\[
\boxed{\text{Organisation} = \text{persistente relationale Rollen-, Abhängigkeits- und Evolutionsstruktur}}
\]

auch wenn sich Geometrie und individuelle Bewegungen stark verändern.

## 2. Konsequenz

Zwei geometrisch deutlich verschiedene Zustände können organisatorisch äquivalent sein:

\[
X_1\neq X_2
\]

während

\[
Z_1\simeq Z_2.
\]

Umgekehrt können zwei geometrisch fast identische Zustände organisatorisch verschieden sein:

\[
X_1\approx X_2
\]

aber

\[
Z_1\not\simeq Z_2.
\]

Daher gilt nicht:

\[
\text{geometric change} \equiv \text{organizational change}.
\]

## 3. Mini-Re-Run als Proof of Concept

Ein kleiner kontrollierter 8-Knoten-Test wurde mit zwei Gegenfällen durchgeführt.

### Fall A — starke Geometrieänderung, gleiche Organisation

Geometrie:

- 47.7% mittlere Paarabstandsänderung
- \(r_{\mathrm{distance}}=0.522\)

Relationen blieben unverändert:

\[
J_{\mathrm{edge}}=1.000.
\]

Normierter Laplace:

\[
\Delta\operatorname{spec}(L_N)=0.
\]

Low-mode Projector:

\[
\|P_1-P_2\|_F=0.
\]

Ergebnis:

\[
\boxed{\text{large geometric change} + \text{organizational invariance}}
\]

### Fall B — nahezu gleiche Geometrie, andere Organisation

Geometrie:

- 2.54% mittlere Paarabstandsänderung
- \(r_{\mathrm{distance}}=0.99874\)

Ein degree-preserving relationaler 2-switch wurde durchgeführt. Dabei blieb sogar

\[
d_i^{(1)}=d_i^{(2)} \qquad\forall i.
\]

Trotzdem:

\[
J_{\mathrm{edge}}=0.636,
\]

\[
\|\Delta\operatorname{spec}(L_N)\|_2=0.4284,
\]

und

\[
\|P_{\mathrm{low2}}^{(1)}-P_{\mathrm{low2}}^{(2)}\|_F=1.152.
\]

Außerdem:

\[
\lambda_2: 0.1750\rightarrow0.3130.
\]

Ergebnis:

\[
\boxed{\text{small geometric change} + \text{large organizational/operator change}}
\]

## 4. Interpretation des Laplacian

Der Laplacian beziehungsweise seine Eigen-/Projektor-Unterräume sollte vorläufig **nicht als direkter Geometrie- oder Schwarmdetektor** interpretiert werden.

Die interessantere Interpretation ist:

\[
\boxed{L\text{ bzw. }L_N \rightarrow \text{Extraktion kollektiver relationaler Modi}}
\]

und insbesondere können niedrigdimensionale spektrale Unterräume Kandidaten für einen **persistenten kollektiven Organisationszustand** darstellen.

Nicht einzelne Eigenvektoren stehen dabei zwingend im Vordergrund, sondern basisinvariante Eigenräume bzw. Projektoren.

## 5. Verbindung zu bisherigen TFL-Ergebnissen

Die Entwicklung

\[
\text{Geometry} \rightarrow \text{Operator} \rightarrow \text{Relation} \rightarrow \text{Organization} \rightarrow \text{State Dynamics}
\]

kann neu interpretiert werden:

Geometrie war möglicherweise nicht der eigentliche Zustandsraum, sondern eine beobachtbare Realisierung einer tieferen relationalen Organisation.

Die bisherigen Ergebnisse unterstützen bereits:

\[
\boxed{\text{Geometry alone is insufficient.}}
\]

und:

\[
\boxed{\text{Relational/operator features retain information not captured by geometry alone.}}
\]

Noch **nicht bewiesen** ist:

\[
\boxed{\text{relational organization is the unique true state variable}.}
\]

## 6. Verbindung zu TRANSPORT-001 bis TRANSPORT-005

Die Transport-Tests zeigten zusätzlich:

\[
\text{gleiche Repräsentation} \not\Rightarrow \text{gleiche Observable},
\]

und sogar

\[
\text{gleiche Repräsentation} \not\Rightarrow \text{gleiche quantitative Ordnung}.
\]

Aggregierte relationale Statistiken reichen ebenfalls nicht zwingend aus.

Entscheidend kann sein:

\[
\boxed{\text{wer mit wem auf welche Weise gekoppelt ist}}
\]

statt lediglich:

\[
\text{wie viele Relationen vorhanden sind}.
\]

Damit wird **Organisation der Relationen** von bloßer Relation unterschieden.

## 7. Bedeutung für Aerlis/UAS

Für koordinierte Systeme wie einen Drohnenschwarm sollte die Analyse nicht primär fragen:

> Wo befindet sich jedes Objekt und wohin bewegt es sich?

sondern zusätzlich:

> Welche relationale Rolle, Abhängigkeit und funktionale Position besitzt jedes Objekt innerhalb des kollektiven Zustands?

Eine Formation kann sich verändern, Ablenkungsbewegungen können stattfinden und individuelle Trajektorien können chaotisch erscheinen, während die zugrunde liegende Organisationsstruktur stabil bleibt.

Daher ist für Aerlis relevant:

\[
\boxed{\text{role/dependency persistence} > \text{raw geometric persistence}}
\]

als zu testende Hypothese, nicht als bereits bewiesener Satz.

## 8. Bedeutung für SPATIAL Orientation

SPATIAL darf räumliche Orientierung nicht automatisch mit Organisationszustand gleichsetzen.

Es müssen mindestens drei Beobachtungsbasen getrennt ausgewertet werden:

\[
\boxed{\text{Geometry} \;|\; \text{Relation} \;|\; \text{Relational eigenspace/projector}}
\]

Der entscheidende Cross-over-Test lautet:

**A**

\[
\text{large geometry change} + \text{preserved relational role}
\]

gegen

**B**

\[
\text{small geometry change} + \text{broken relational role}.
\]

Wenn der relationale/Projektor-Raum A als stabil und B als verändert erkennt, während die geometrische Basis das Gegenteil nahelegt, ist dies Evidenz dafür, dass Organisation näher am invarianten Zustand liegt als Geometrie.

## 9. Codex-Gate

Noch **kein vollständiges Neuaufrollen** der alten TFL/RDL-Daten.

Zuerst ein begrenzter Codex-Pilot mit einem alten echten Datensatz und paralleler Auswertung:

\[
G=\text{geometry features}
\]

\[
R=\text{relational features}
\]

\[
P=\text{spectral/projector features}.
\]

Primäre Frage:

\[
\boxed{\text{Welche Basis bleibt stabil unter geometry-preserving/organization-breaking und geometry-breaking/organization-preserving perturbations?}}
\]

Erst wenn der Cross-over in echten alten Daten reproduziert wird:

\[
\boxed{\text{GO: systematic TFL/RDL re-analysis}}
\]

ansonsten:

\[
\boxed{\text{NO-GO: retain as toy-model observation}}
\]

## Canonical Working Statement

\[
\boxed{\textbf{Geometry describes where the system is realized.}}
\]

\[
\boxed{\textbf{Relational organization may describe what collective state the system is in.}}
\]

**Snapshot-ID:** `TFL-ORG-SNAPSHOT-001`
