(function () {
  'use strict';

  var state = {
    payload: null,
    metric: 'hrv_ms',
    view: 'care'
  };

  var metricMeta = {
    hrv_ms: {
      tab: 'HRV',
      axis: 'HRV (ms)',
      unit: 'ms',
      digits: 1,
      padding: 3
    },
    sleep_hours: {
      tab: 'Sleep',
      axis: 'Sleep (hours)',
      unit: 'h',
      digits: 2,
      padding: 0.25
    }
  };

  function fmt(value, digits) {
    var precision = digits == null ? 2 : digits;
    return typeof value === 'number' && Number.isFinite(value) ? value.toFixed(precision) : '—';
  }

  function signed(value, digits) {
    return typeof value === 'number' && Number.isFinite(value) ? (value >= 0 ? '+' : '') + fmt(value, digits) : '—';
  }

  function escapeText(value) {
    return String(value).replace(/[&<>"']/g, function (character) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character];
    });
  }

  function displayCopy(value) {
    if (typeof value === 'string') return escapeText(value);
    if (Array.isArray(value)) return value.map(displayCopy);
    if (value && typeof value === 'object') {
      return Object.fromEntries(Object.entries(value).map(function (entry) {
        return [entry[0], displayCopy(entry[1])];
      }));
    }
    return value;
  }

  function shortDate(value) {
    return new Date(value + 'T12:00:00').toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric'
    });
  }

  function dayLabel(value) {
    return new Date(value + 'T12:00:00').toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    });
  }

  function sourceRow(label, value, description) {
    return [
      '<div class="source-row">',
      '<span>', label, '</span>',
      '<div><strong>', value, '</strong><p>', description, '</p></div>',
      '</div>'
    ].join('');
  }

  function render(payload) {
    state.payload = payload;
    payload = displayCopy(payload);
    var a = payload.analysis;
    var p = payload.plan;
    var brief = payload.care_brief;
    var primary = a.primary_effect;
    var readiness = brief.readiness;
    var labs = a.longevity_snapshot || {};
    var genome = a.genomics_context || {};
    var sleep = a.secondary_effects.find(function (item) {
      return item.outcome === 'sleep_hours';
    }) || {};
    var rhr = a.secondary_effects.find(function (item) {
      return item.outcome === 'resting_hr';
    }) || {};

    var schedule = p.schedule.map(function (day) {
      var conditionClass = day.condition.indexOf('Cutoff') === 0 ? 'cutoff' : 'usual';
      return [
        '<div class="day ', conditionClass, '">',
        '<strong>', dayLabel(day.date), '</strong>',
        '<span>', day.condition, '</span>',
        '</div>'
      ].join('');
    }).join('');

    var controls = p.controls.map(function (item) {
      return [
        '<div class="control">',
        '<div class="check" aria-hidden="true">&#10003;</div>',
        '<div>', item, '</div>',
        '</div>'
      ].join('');
    }).join('');

    var stopConditions = p.stop_conditions.map(function (item) {
      return '<li>' + item + '</li>';
    }).join('');

    var warnings = a.quality.warnings.map(function (item) {
      return '<div class="warning">' + item + '</div>';
    }).join('');

    var calculations = a.calculation_provenance.map(function (item) {
      return '<div>' + item + '</div>';
    }).join('');

    var careSources = brief.source_ledger.map(function (source) {
      var coverage = Object.entries(source.coverage || {}).map(function (entry) {
        var names = { hrv_ms: 'HRV', sleep_hours: 'sleep', resting_hr: 'resting HR', caffeine_cutoff_2pm: 'timing', caffeine_mg: 'dose', training_load: 'training', alcohol_units: 'alcohol' };
        return (names[entry[0]] || entry[0]) + ': ' + entry[1];
      }).join(' · ');
      return [
        '<div class="care-source">',
        '<div><span>', source.label, '</span><strong>', source.status, '</strong></div>',
        '<div><p>', source.provenance, '</p><p class="source-role">', source.role, '</p>',
        coverage ? '<p class="source-coverage">Recorded values — ' + coverage + '</p>' : '',
        source.url && /^https?:\/\//.test(source.url) ? '<a href="' + source.url + '" target="_blank" rel="noreferrer">Inspect source<span class="sr-only">: ' + source.label + '</span> ↗</a>' : '<span class="source-unlinked">No source link supplied</span>',
        '</div>',
        '</div>'
      ].join('');
    }).join('');

    var uncertainty = brief.uncertainty.map(function (item) {
      return '<li>' + item + '</li>';
    }).join('');

    var missingEvidence = brief.missing_evidence.map(function (item) {
      return '<li>' + item + '</li>';
    }).join('');

    var clinicianQuestions = brief.questions_for_clinician.map(function (item, index) {
      return [
        '<li><span>', String(index + 1).padStart(2, '0'), '</span><p>', item, '</p></li>'
      ].join('');
    }).join('');

    document.getElementById('app').innerHTML = [
      '<section class="view" id="view-overview" data-view-panel="overview">',
        '<div class="page-intro">',
          '<p class="kicker">Maya&#39;s current question</p>',
          '<h1>', a.question, '</h1>',
          '<p>Compare one daily habit with the following night&#39;s recovery, then turn the signal into a controlled retest.</p>',
        '</div>',

        '<div class="result-band">',
          '<div class="primary-result">',
            '<div class="label">Observed HRV difference</div>',
            '<div class="result-value">', signed(primary.effect), ' ms</div>',
            '<p class="result-copy">', brief.signal_headline, '.</p>',
            '<div class="result-meta">',
              '<span class="claim-pill">Association only</span>',
              '<span>95% interval ', signed(primary.ci_low), ' to ', signed(primary.ci_high), '</span>',
            '</div>',
          '</div>',
          '<div class="supporting-metrics">',
            '<div class="support-metric">',
              '<div class="label">Sleep duration</div>',
              '<strong>', signed(sleep.effect), ' h</strong>',
              '<p>Difference between cutoff and usual-timing nights.</p>',
            '</div>',
            '<div class="support-metric">',
              '<div class="label">Resting HR</div>',
              '<strong>', signed(rhr.effect), ' bpm</strong>',
              '<p>Difference between cutoff and usual-timing nights.</p>',
            '</div>',
            '<div class="support-metric">',
              '<div class="label">Paired nights</div>',
              '<strong>', a.quality.paired_days, '</strong>',
              '<p>', a.quality.condition_on_n, ' cutoff and ', a.quality.condition_off_n, ' usual-timing observations.</p>',
            '</div>',
          '</div>',
        '</div>',

        '<section class="journey" aria-labelledby="journey-heading">',
          '<div class="section-bar">',
            '<div><h2 id="journey-heading">How we got here</h2><p>One question, one comparison, one next step.</p></div>',
          '</div>',
          '<div class="journey-grid">',
            '<button class="journey-step" type="button" data-go="overview">',
              '<span class="step-index">01 &middot; Habit</span>',
              '<span class="step-value">Caffeine by 2 PM</span>',
              '<span class="step-note">Compared with usual timing</span>',
            '</button>',
            '<button class="journey-step" type="button" data-go="data">',
              '<span class="step-index">02 &middot; Comparison</span>',
              '<span class="step-value">', a.quality.paired_days, ' paired nights</span>',
              '<span class="step-note">', a.quality.condition_on_n, ' cutoff / ', a.quality.condition_off_n, ' usual</span>',
            '</button>',
            '<button class="journey-step" type="button" data-open-method="true">',
              '<span class="step-index">03 &middot; Signal</span>',
              '<span class="step-value">', signed(primary.effect), ' ms HRV</span>',
              '<span class="step-note">95% interval ', signed(primary.ci_low), ' to ', signed(primary.ci_high), '</span>',
            '</button>',
            '<button class="journey-step" type="button" data-go="experiment">',
              '<span class="step-index">04 &middot; Next test</span>',
              '<span class="step-value">14-day crossover</span>',
              '<span class="step-note">Predefined controls and decision rule</span>',
            '</button>',
          '</div>',
        '</section>',

        '<div class="overview-grid">',
          '<section class="workspace" aria-labelledby="timeline-heading">',
            '<div class="chart-toolbar">',
              '<div><h2 id="timeline-heading">Recovery timeline</h2><p>Nightly recovery by prior-day caffeine timing</p></div>',
              '<div class="segmented" aria-label="Chart metric">',
                '<button class="active" type="button" data-metric="hrv_ms" aria-pressed="true">HRV</button>',
                '<button type="button" data-metric="sleep_hours" aria-pressed="false">Sleep</button>',
              '</div>',
            '</div>',
            '<div class="chart-wrap">',
              '<svg id="chart" viewBox="0 0 760 250" role="img" aria-labelledby="chart-title chart-description"></svg>',
              '<div class="chart-tooltip" id="chart-tooltip" role="status" hidden></div>',
            '</div>',
            '<div class="legend">',
              '<span><i style="background:var(--green)"></i>Cutoff by 2 PM</span>',
              '<span><i style="background:var(--coral)"></i>Usual timing</span>',
              '<span><i style="background:#87959a"></i>Timing unavailable</span>',
              '<span><i class="line-key"></i>7-calendar-day mean</span>',
            '</div>',
          '</section>',

          '<aside class="reading-panel">',
            '<h2>What this means</h2>',
            '<p>', brief.plain_language_signal, '</p>',
            '<div class="reading-facts">',
              '<div class="reading-fact"><span>Coverage</span><strong>', Math.round(a.quality.coverage * 100), '% of calendar days</strong></div>',
              '<div class="reading-fact"><span>Balance</span><strong>', a.quality.condition_on_n, ' vs ', a.quality.condition_off_n, ' nights</strong></div>',
              '<div class="reading-fact"><span>Data grade</span><strong>', a.quality.grade, ' &middot; ', a.quality.score, '/100</strong></div>',
            '</div>',
            '<div class="actions">',
              '<button class="button primary" type="button" data-go="care">Prepare care brief</button>',
              '<button class="button" type="button" data-go="experiment">View 14-day retest</button>',
            '</div>',
          '</aside>',
        '</div>',
      '</section>',

      '<section class="view" id="view-care" data-view-panel="care" hidden>',
        '<div class="care-titlebar">',
          '<div class="page-intro">',
            '<p class="kicker">Care brief &middot; draft for review</p>',
            '<h1>Personal evidence, ready for review.</h1>',
            '<p>A concise, source-linked summary a person can review before deciding whether to share it with a clinician.</p>',
          '</div>',
          '<div class="care-actions">',
            '<div class="export-buttons"><button class="button primary" type="button" data-export="markdown">Download Markdown</button>',
            '<button class="button" type="button" data-export="json">Download JSON</button>',
            '<button class="button" type="button" data-print-brief="true">Print brief</button></div>',
            '<span>Save locally. Sources and warnings stay attached.</span>',
            '<span id="export-status" role="status" aria-live="polite"></span>',
          '</div>',
        '</div>',

        '<article class="care-sheet" id="care-sheet" aria-labelledby="care-question">',
          '<header class="care-sheet-head">',
            '<div>',
              '<span class="document-label">LiveForever personal evidence brief</span>',
              '<h2 id="care-question">', brief.visit_question, '</h2>',
              '<p>', brief.why_this_visit, '</p>',
            '</div>',
            '<dl>',
              '<div><dt>Person</dt><dd>', brief.persona, '</dd></div>',
              '<div><dt>Record</dt><dd>', brief.privacy.record_type, '</dd></div>',
              '<div><dt>Window</dt><dd>', a.dataset.start_date || 'Not supplied', ' — ', a.dataset.end_date || 'Not supplied', '</dd></div>',
            '</dl>',
          '</header>',

          '<section class="care-readiness" aria-labelledby="readiness-heading">',
            '<div class="readiness-heading"><span class="status-dot ', readiness.status, '" aria-hidden="true"></span><div><span class="document-label">Evidence readiness</span><h3 id="readiness-heading">', readiness.label, '</h3></div></div>',
            '<dl class="readiness-facts">',
              '<div><dt>Paired nights</dt><dd>', primary.n_on + primary.n_off, '<small>', primary.n_on, ' cutoff / ', primary.n_off, ' usual</small></dd></div>',
              '<div><dt>Sources supplied</dt><dd>', readiness.sources_supplied, ' / ', readiness.sources_total, '<small>', readiness.core_sources_linked ? 'Comparison sources linked' : 'Comparison source links missing', '</small></dd></div>',
              '<div><dt>Quality warnings</dt><dd>', readiness.warning_count, '<small>Grade ', a.quality.grade, ' · ', a.quality.score, '/100</small></dd></div>',
            '</dl>',
            '<p class="readiness-boundary">', readiness.boundary, '</p>',
          '</section>',

          '<section class="care-signal ', readiness.signal === 'higher' && readiness.status === 'reviewable' ? '' : 'signal-neutral', '" aria-labelledby="care-signal-heading">',
            '<div>',
              '<span class="document-label">Observed signal</span>',
              '<h3 id="care-signal-heading">', brief.signal_headline, '</h3>',
              '<p>', brief.plain_language_signal, '</p>',
            '</div>',
            '<div class="care-lock">',
              '<span aria-hidden="true">&#10003;</span>',
              '<p><strong>Values locked by code</strong>AI can explain this result, but cannot rewrite its effect, interval, samples, or sources.</p>',
            '</div>',
          '</section>',

          '<div class="care-columns">',
            '<section class="care-block" aria-labelledby="care-source-heading">',
              '<div class="care-block-head"><span>01</span><div><h3 id="care-source-heading">Sources supplied</h3><p>Inspect the record, coverage, and role of each source.</p></div></div>',
              '<div class="care-source-list">', careSources, '</div>',
            '</section>',

            '<section class="care-block" aria-labelledby="care-uncertainty-heading">',
              '<div class="care-block-head"><span>02</span><div><h3 id="care-uncertainty-heading">What remains uncertain</h3><p>Limitations travel with the summary.</p></div></div>',
              '<ul class="care-list">', uncertainty, '</ul>',
              '<div class="brief-warnings"><h4>Quality warnings</h4>', warnings, '</div>',
              '<details class="missing-details">',
                '<summary>Missing evidence to consider</summary>',
                '<ul>', missingEvidence, '</ul>',
              '</details>',
            '</section>',
          '</div>',

          '<section class="care-block care-supporting" aria-labelledby="supporting-heading">',
            '<h3 id="supporting-heading">Supporting outcomes</h3><p>Cutoff minus usual timing; each outcome has its own paired sample.</p>',
            '<div class="evidence-table-wrap"><table class="evidence-table"><thead><tr><th scope="col">Outcome</th><th scope="col">Difference</th><th scope="col">95% interval</th><th scope="col">Cutoff / usual</th></tr></thead><tbody>',
              '<tr><th scope="row">Sleep duration</th><td>', signed(sleep.effect), ' h</td><td>', signed(sleep.ci_low), ' to ', signed(sleep.ci_high), '</td><td>', sleep.n_on == null ? '—' : sleep.n_on, ' / ', sleep.n_off == null ? '—' : sleep.n_off, '</td></tr>',
              '<tr><th scope="row">Resting HR</th><td>', signed(rhr.effect), ' bpm</td><td>', signed(rhr.ci_low), ' to ', signed(rhr.ci_high), '</td><td>', rhr.n_on == null ? '—' : rhr.n_on, ' / ', rhr.n_off == null ? '—' : rhr.n_off, '</td></tr>',
            '</tbody></table></div>',
          '</section>',

          '<section class="care-questions" aria-labelledby="care-questions-heading">',
            '<div class="care-block-head"><span>03</span><div><h3 id="care-questions-heading">Questions for a clinician</h3><p>The AI prepares the agenda; the clinician supplies medical judgment.</p></div></div>',
            '<ol>', clinicianQuestions, '</ol>',
          '</section>',

          '<footer class="care-sheet-foot">',
            '<div><strong>User-controlled handoff</strong><p>', brief.privacy.sharing_control, '</p></div>',
            '<div><strong>Boundary</strong><p>', brief.review_status, '</p></div>',
          '</footer>',
        '</article>',

        '<section class="ai-role-band" aria-labelledby="ai-role-heading">',
          '<div>',
            '<p class="kicker">Bounded AI layer</p>',
            '<h2 id="ai-role-heading">AI prepares the review. It does not own the evidence.</h2>',
            '<p>', brief.ai_contract.role, ' ', brief.ai_contract.human_gate, '</p>',
          '</div>',
          '<button class="button" type="button" data-open-method="true">Inspect the contract</button>',
        '</section>',
      '</section>',

      '<section class="view" id="view-experiment" data-view-panel="experiment" hidden>',
        '<div class="page-intro">',
          '<p class="kicker">14-day retest</p>',
          '<h1>Retest the signal under a balanced schedule.</h1>',
          '<p>Alternate cutoff and usual-timing days while keeping the major inputs steady.</p>',
        '</div>',
        '<div class="experiment-layout">',
          '<section class="schedule-panel" aria-labelledby="schedule-heading">',
            '<div class="schedule-head">',
              '<div><h2 id="schedule-heading">', p.title, '</h2><p>', p.design, '</p></div>',
              '<div class="schedule-key">',
                '<span><i style="background:var(--green)"></i>Cutoff</span>',
                '<span><i style="background:var(--coral)"></i>Usual</span>',
              '</div>',
            '</div>',
            schedule ? '<div class="schedule">' + schedule + '</div>' : '<p class="panel-lede">No dated schedule is available because no observation window was supplied.</p>',
          '</section>',
          '<aside class="controls-panel">',
            '<h2>Predefined controls</h2>',
            controls,
            '<div class="decision"><strong>Decision rule</strong>', p.decision_rule, '</div>',
            '<details class="pause-details">',
              '<summary>When to pause</summary>',
              '<ul>', stopConditions, '</ul>',
            '</details>',
          '</aside>',
        '</div>',
      '</section>',

      '<section class="view" id="view-data" data-view-panel="data" hidden>',
        '<div class="page-intro">',
          '<p class="kicker">Data and methods</p>',
          '<h1>Know what is behind the number.</h1>',
          '<p>Inspect completeness, context, and calculation details without crowding the primary result.</p>',
        '</div>',

        '<div class="quality-strip" aria-label="Data quality summary">',
          '<div class="quality-stat"><div class="label">Evidence grade</div><strong>', a.quality.grade, '</strong><p>', a.quality.score, ' out of 100</p></div>',
          '<div class="quality-stat"><div class="label">Calendar coverage</div><strong>', Math.round(a.quality.coverage * 100), '%</strong><p>', a.dataset.recorded_days, ' fictional recorded days</p></div>',
          '<div class="quality-stat"><div class="label">Cutoff nights</div><strong>', a.quality.condition_on_n, '</strong><p>Paired with next-day outcomes</p></div>',
          '<div class="quality-stat"><div class="label">Usual nights</div><strong>', a.quality.condition_off_n, '</strong><p>Paired with next-day outcomes</p></div>',
        '</div>',

        '<div class="data-layout">',
          '<section class="quality-panel">',
            '<h2>Connected data</h2>',
            '<p class="panel-lede">', readiness.sources_supplied, ' of ', readiness.sources_total, ' source layers supplied. Laboratory and genomic context are excluded from the observed effect.</p>',
            '<div class="source-list">',
              sourceRow('Wearables', a.dataset.recorded_days + ' daily records', 'HRV, sleep duration, resting heart rate, and missingness.'),
              sourceRow('Habit log', a.quality.paired_days + ' paired nights', 'Caffeine timing, total dose, training load, meditation, and alcohol.'),
              sourceRow('Laboratory', labs.completeness || 'Not supplied', 'Context for the published PhenoAge calculation.'),
              sourceRow('Genomics', genome.confidence || 'Not supplied', 'Caffeine-metabolism context used to prioritize the question.'),
            '</div>',
            '<div class="warning-list">', warnings, '</div>',
          '</section>',

          '<aside class="context-panel">',
            '<h2>Personal context</h2>',
            '<p class="panel-lede">Context helps choose what to test. The observed data still owns the result.</p>',
            '<div class="context-item">',
              '<div class="context-value">', genome.gene || '—', '<br>', genome.synthetic_genotype || '—', '</div>',
              '<div class="context-copy"><strong>Caffeine metabolism context</strong><p>', genome.annotation || 'No genomic context was supplied for this run.', '</p></div>',
            '</div>',
            '<div class="context-item">',
              '<div class="context-value">', fmt(labs.phenoage, 1), '<br>yrs</div>',
              '<div class="context-copy"><strong>PhenoAge snapshot</strong><p>', labs.completeness ? 'Chronological age ' + fmt(labs.chronological_age, 0) + '; difference ' + signed(labs.difference_years, 1) + ' years. Calculated from ' + labs.completeness.toLowerCase() + '.' : 'No laboratory snapshot was supplied for this run.', '</p></div>',
            '</div>',
          '</aside>',

          '<section class="method-panel">',
            '<h2>Calculation method</h2>',
            '<p class="panel-lede">Deterministic Python produces every displayed value. The LiveForever Codex Skill uses GPT-5.6 to explain the result and adapt the retest without changing the calculations.</p>',
            '<details class="method-details" id="method-details">',
              '<summary>Show calculation and provenance</summary>',
              '<div class="method-content">',
                '<div class="formula-list">', calculations, '</div>',
                '<p><strong>Primary estimate:</strong> ', signed(primary.effect), ' ms, 95% interval ', signed(primary.ci_low), ' to ', signed(primary.ci_high), ', from ', primary.n_on, ' cutoff and ', primary.n_off, ' usual-timing paired nights.</p>',
                '<p>', a.claim_boundary, '</p>',
              '</div>',
            '</details>',
          '</section>',
        '</div>',

        '<div class="privacy-band">',
          '<div><strong>Privacy by design</strong><p>Every record in this public demo is synthetic. No login, external health service, API key, or personal health data is used.</p></div>',
          '<a class="button" href="https://github.com/bakulbadwal/liveforever-care-brief" target="_blank" rel="noreferrer">View source</a>',
        '</div>',
      '</section>'
    ].join('');

    bindControls();
    drawChart(a.timeline, state.metric);

    var initialView = window.location.hash.replace('#', '');
    setView(['overview', 'care', 'experiment', 'data'].indexOf(initialView) >= 0 ? initialView : 'care', false);
  }

  function bindControls() {
    document.querySelectorAll('[data-metric]').forEach(function (button) {
      button.addEventListener('click', function () {
        state.metric = button.dataset.metric;
        document.querySelectorAll('[data-metric]').forEach(function (item) {
          var active = item === button;
          item.classList.toggle('active', active);
          item.setAttribute('aria-pressed', String(active));
        });
        drawChart(state.payload.analysis.timeline, state.metric);
      });
    });

    document.querySelectorAll('[data-go]').forEach(function (button) {
      button.addEventListener('click', function () {
        navigate(button.dataset.go);
      });
    });

    document.querySelectorAll('[data-open-method]').forEach(function (button) {
      button.addEventListener('click', function () {
        navigate('data');
        var method = document.getElementById('method-details');
        method.open = true;
        method.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });
    });

    document.querySelectorAll('[data-print-brief]').forEach(function (button) {
      button.addEventListener('click', function () {
        window.print();
      });
    });

    document.querySelectorAll('[data-export]').forEach(function (button) {
      button.addEventListener('click', function () {
        var format = button.dataset.export;
        var brief = state.payload.care_brief;
        var status = document.getElementById('export-status');
        var text = format === 'json' ? JSON.stringify(brief, null, 2) + '\n' : (state.payload.exports || {}).care_brief_markdown;
        if (!text) {
          status.textContent = 'This format is unavailable. Rebuild the demo with the current evidence engine.';
          return;
        }
        var extension = format === 'json' ? 'json' : 'md';
        var name = 'liveforever-care-brief-' + (brief.evidence_summary.data_window.end_date || 'undated') + '.' + extension;
        var url = URL.createObjectURL(new Blob([text], { type: format === 'json' ? 'application/json;charset=utf-8' : 'text/markdown;charset=utf-8' }));
        var link = document.createElement('a');
        link.href = url;
        link.download = name;
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
        status.textContent = 'Download requested: ' + name + '. Includes all evidence, sources, and warnings.';
      });
    });
  }

  function navigate(view) {
    if (window.location.hash !== '#' + view) {
      window.history.pushState({ view: view }, '', '#' + view);
    }
    setView(view, true);
  }

  function setView(view, focusHeading) {
    state.view = view;

    document.querySelectorAll('[data-view-panel]').forEach(function (panel) {
      var active = panel.dataset.viewPanel === view;
      panel.classList.toggle('active', active);
      panel.hidden = !active;
    });

    document.querySelectorAll('[data-view]').forEach(function (button) {
      var active = button.dataset.view === view;
      button.classList.toggle('active', active);
      button.setAttribute('aria-current', active ? 'page' : 'false');
    });

    if (focusHeading) {
      var heading = document.querySelector('[data-view-panel="' + view + '"] h1');
      if (heading) {
        heading.setAttribute('tabindex', '-1');
        heading.focus({ preventScroll: true });
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  function movingAverage(timeline, metric, index) {
    var end = Date.parse(timeline[index].date);
    var slice = timeline.slice(0, index + 1).filter(function (point) {
      return Date.parse(point.date) >= end - 6 * 86400000 && typeof point[metric] === 'number' && Number.isFinite(point[metric]);
    }).map(function (point) { return point[metric]; });

    if (!slice.length) {
      return null;
    }

    return slice.reduce(function (sum, value) {
      return sum + value;
    }, 0) / slice.length;
  }

  function drawChart(timeline, metric) {
    var svg = document.getElementById('chart');
    if (!svg) {
      return;
    }

    var meta = metricMeta[metric];
    var values = timeline.map(function (point) { return point[metric]; });
    var valid = values.filter(function (value) { return typeof value === 'number' && Number.isFinite(value); });
    document.getElementById('chart-tooltip').hidden = true;
    if (!valid.length) {
      svg.innerHTML = '<title id="chart-title">Recovery timeline unavailable</title><desc id="chart-description">No recorded values for this metric.</desc><text x="380" y="125" text-anchor="middle" fill="#627176" font-size="14">No recorded values for this metric</text>';
      return;
    }
    var min = Math.min.apply(null, valid) - meta.padding;
    var max = Math.max.apply(null, valid) + meta.padding;
    var left = 48;
    var right = 742;
    var top = 22;
    var bottom = 208;
    var firstDate = Date.parse(timeline[0].date);
    var timeSpan = Date.parse(timeline[timeline.length - 1].date) - firstDate;
    var x = function (index) {
      return left + (right - left) * (Date.parse(timeline[index].date) - firstDate) / Math.max(1, timeSpan);
    };
    var y = function (value) {
      return bottom - (value - min) / (max - min) * (bottom - top);
    };

    var averages = values.map(function (_, index) {
      return movingAverage(timeline, metric, index);
    });

    var pathParts = [];
    var started = false;
    averages.forEach(function (value, index) {
      if (value == null) {
        started = false;
        return;
      }
      pathParts.push((started ? 'L' : 'M') + x(index).toFixed(1) + ',' + y(value).toFixed(1));
      started = true;
    });

    var grid = [0, 0.25, 0.5, 0.75, 1].map(function (fraction) {
      var value = max - (max - min) * fraction;
      var yy = top + (bottom - top) * fraction;
      var label = metric === 'hrv_ms' ? value.toFixed(0) : value.toFixed(1);
      return [
        '<line x1="', left, '" y1="', yy, '" x2="', right, '" y2="', yy, '" stroke="#d6dfdc"/>',
        '<text x="', left - 9, '" y="', yy + 4, '" text-anchor="end" fill="#627176" font-size="10">', label, '</text>'
      ].join('');
    }).join('');

    var dots = timeline.map(function (point, index) {
      if (typeof point[metric] !== 'number' || !Number.isFinite(point[metric])) {
        return '';
      }
      var timing = point.prior_day_caffeine_cutoff_2pm;
      var condition = timing == null ? 'Prior-day timing unavailable' : timing >= 0.5 ? 'Prior-day cutoff by 2 PM' : 'Prior-day usual timing';
      return [
        '<circle class="chart-point" tabindex="0" data-index="', index, '" ',
        'cx="', x(index), '" cy="', y(point[metric]), '" r="4.5" ',
        'fill="', timing == null ? '#87959a' : timing >= 0.5 ? '#14745f' : '#c45b49', '" ',
        'stroke="#ffffff" stroke-width="1.5">',
        '<title>', shortDate(point.date), ': ', fmt(point[metric], meta.digits), ' ', meta.unit, '. ', condition, '</title>',
        '</circle>'
      ].join('');
    }).join('');

    var dateIndexes = Array.from(new Set([0, Math.floor((timeline.length - 1) / 2), timeline.length - 1]));
    var dates = dateIndexes.map(function (index) {
      return [
        '<text x="', x(index), '" y="234" text-anchor="middle" fill="#627176" font-size="10">',
        shortDate(timeline[index].date),
        '</text>'
      ].join('');
    }).join('');

    svg.innerHTML = [
      '<title id="chart-title">Recovery timeline</title>',
      '<desc id="chart-description">', meta.axis, ' by prior-day caffeine timing. Use Tab to inspect individual points.</desc>',
      grid,
      '<path d="', pathParts.join(' '), '" fill="none" stroke="#87959a" stroke-width="2.5"/>',
      dots,
      dates,
      '<text x="', left, '" y="13" fill="#627176" font-size="10">', meta.axis, '</text>'
    ].join('');

    bindChartTooltips(timeline, metric);
  }

  function bindChartTooltips(timeline, metric) {
    var tooltip = document.getElementById('chart-tooltip');
    var wrapper = tooltip.parentElement;
    var meta = metricMeta[metric];

    function show(event) {
      var circle = event.currentTarget;
      var point = timeline[Number(circle.dataset.index)];
      var circleRect = circle.getBoundingClientRect();
      var wrapperRect = wrapper.getBoundingClientRect();
      var timing = point.prior_day_caffeine_cutoff_2pm;
      var condition = timing == null ? 'Prior-day timing unavailable' : timing >= 0.5 ? 'Prior-day cutoff by 2 PM' : 'Prior-day usual timing';

      tooltip.innerHTML = [
        '<strong>', shortDate(point.date), '</strong><br>',
        fmt(point[metric], meta.digits), ' ', meta.unit, '<br>',
        condition
      ].join('');
      tooltip.hidden = false;

      var desiredLeft = circleRect.left - wrapperRect.left + circleRect.width + 10;
      var desiredTop = circleRect.top - wrapperRect.top - 16;
      tooltip.style.left = Math.min(Math.max(8, desiredLeft), wrapperRect.width - tooltip.offsetWidth - 8) + 'px';
      tooltip.style.top = Math.min(Math.max(8, desiredTop), wrapperRect.height - tooltip.offsetHeight - 8) + 'px';
    }

    function hide() {
      tooltip.hidden = true;
    }

    document.querySelectorAll('.chart-point').forEach(function (circle) {
      circle.addEventListener('pointerenter', show);
      circle.addEventListener('pointermove', show);
      circle.addEventListener('focus', show);
      circle.addEventListener('pointerleave', hide);
      circle.addEventListener('blur', hide);
    });
  }

  document.querySelectorAll('[data-view]').forEach(function (button) {
    button.addEventListener('click', function () {
      navigate(button.dataset.view);
    });
  });

  window.addEventListener('popstate', function () {
    var view = window.location.hash.replace('#', '') || 'care';
    if (['overview', 'care', 'experiment', 'data'].indexOf(view) >= 0) {
      setView(view, false);
    }
  });

  var printDetails = [];
  window.addEventListener('beforeprint', function () {
    printDetails = Array.from(document.querySelectorAll('#care-sheet details:not([open])'));
    printDetails.forEach(function (detail) { detail.open = true; });
  });
  window.addEventListener('afterprint', function () {
    printDetails.forEach(function (detail) { detail.open = false; });
  });

  fetch('analysis.json')
    .then(function (response) {
      if (!response.ok) {
        throw new Error('Could not load analysis (' + response.status + ')');
      }
      return response.json();
    })
    .then(render)
    .catch(function (error) {
      document.getElementById('app').innerHTML = [
        '<div class="error-state">',
        '<strong>Demo data could not load.</strong>',
        escapeText(error.message),
        '<br><br>Serve the demo folder over HTTP rather than opening the file directly.',
        '</div>'
      ].join('');
    });
})();
