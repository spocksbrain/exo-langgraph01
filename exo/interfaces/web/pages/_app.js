import '../styles/globals.css'
import Head from 'next/head'

function ExoApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>exo - Multi-Agent System</title>
        <meta name="description" content="exo multi-agent AI system" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Component {...pageProps} />
    </>
  )
}

export default ExoApp
