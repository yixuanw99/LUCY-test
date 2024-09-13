<template>
    <div id="app">
        <EpigeneticReport />
    </div>
</template>

<script>
import EpigeneticReport from './views/EpigeneticReport.vue'

export default {
    name: 'App',
    components: {
        EpigeneticReport
    }
}
</script>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@100..900&family=Nova+Mono&display=swap');
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        background-color: #f4f4f4;
        margin: 0;
        padding: 20px;
    }

    .header {
        background-color: #a2def4;
        border: 4px solid #80c2ec;
        border-radius: 20px;
        padding: 10px 10px 20px 10px;
        margin-bottom: 20px;
    }

    .header-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 0 10px 10px;
    }

    .header h1 {
        color: #343434;
        margin: 0 0 10px 0;
        font-size: 36px;
        font-family: "Noto Sans TC", sans-serif;
        font-optical-sizing: auto;
        flex-grow: 3;
    }

    .logo-container {
        display: flex;
        align-items: center;
        padding: 0 25px 0 0;
    }

    .logo {
        width: 50px;
        height: auto;
        margin-right: 5px; /* 添加一些右邊距 */
    }

    .logo-text {
        color: #343434;
        font-family: "Nova Mono", sans-serif;
        font-size: 32px; /* 調整字體大小 */
        margin: 0; /* 移除默認邊距 */
    }

    .header-info {
        display: grid;
        grid-template-columns: auto auto;
        gap: 10px;
        justify-content: space-between;
        padding: 0 200px 0 10px;
    }

    .header-info p {
        font-size: 22px;
        margin: 0;
        color: #2b2b2b;
    }

    .container {
        max-width: 800px;
        margin: auto;
        background: #fff;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    h1, h2, h3 {
        color: #333;
    }

    .section {
        margin: 50px 0;
    }

    .section-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .section-title h2 {
        font-size: 26px;
        margin: 0;
    }

    .section-content {
        display: flex;
        align-items: center;
        width: 100%;
    }

    .section-text {
        flex: 1;
    }

    .section-figure {
        flex: 1;
    }

    .cta {
        padding: 1% 1% 0% 1%;
        border: 1px outset;
        color: #303030;
        text-decoration: none;
        border-radius: 5px;
        margin: 0;
    }

    .cta:hover {
        background: #80c2ec;
    }
</style>