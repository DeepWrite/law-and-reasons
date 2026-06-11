---
title: "Historical Issues"
subtitle: "Retrospective legal philosophy and legal theory reviews reconstructed at five-year intervals"
permalink: /historical/
---

Historical issues are one track of 법과 이유 / Law and Reasons. Each historical issue is labeled by target year. Most issues remain in `proposed` status until source mapping, bibliography, private access reviews, drafting, translation, and publication are separately approved. Historical Issue: 2025 is temporarily public as a model issue.

{% assign historical_issues = site.historical_issues | sort: "target_year" | reverse %}

<div class="historical-list">
{% for issue in historical_issues %}
  {% unless issue.listed == false %}
  <article class="historical-list-item">
    <a href="{{ issue.url | relative_url }}">
      <span>{{ issue.historical_status }}</span>
      <h2>Historical Issue: {{ issue.target_year }}</h2>
      <p>{{ issue.coverage_note }}</p>
    </a>
  </article>
  {% endunless %}
{% endfor %}
</div>
